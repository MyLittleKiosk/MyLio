package com.ssafy.mylio.domain.order.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.ssafy.mylio.domain.menu.repository.MenuRepository;
import com.ssafy.mylio.domain.options.entity.MenuOptionMap;
import com.ssafy.mylio.domain.options.entity.OptionDetail;
import com.ssafy.mylio.domain.options.repository.MenuOptionRepository;
import com.ssafy.mylio.domain.order.dto.common.OptionDetailsDto;
import com.ssafy.mylio.domain.order.dto.common.OptionsDto;
import com.ssafy.mylio.domain.order.dto.response.ContentsResponseDto;
import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class OrderValidator {

    private final MenuRepository menuRepository;
    private final MenuOptionRepository menuOptionRepository;
    private final GptPromptService gptPromptService;   // 🔹 추가 – GPT 호출 래퍼

    private final ObjectMapper snakeMapper = new ObjectMapper()
            .setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE);

    /** 리액티브 진입점 */
    public Mono<OrderResponseDto> validate(String pyJson) {
        return Mono.fromCallable(() -> parseAndValidate(pyJson))
                .subscribeOn(Schedulers.boundedElastic());
    }

    // ------------------------------------------------------------
    //  트랜잭션 내부: 파싱 → 검증 → 누락 옵션 프롬프트 생성
    // ------------------------------------------------------------

    @Transactional(readOnly = true)
    protected OrderResponseDto parseAndValidate(String json) {
        OrderResponseDto order = parsePythonPayload(json);

        List<String> missingOpts = new ArrayList<>();
        List<ContentsResponseDto> fixedContents = order.getContents().stream()
                .map(c -> validateAndCorrect(c, missingOpts))
                .toList();

        if (!missingOpts.isEmpty()) {
            String reply = gptPromptService.buildAskRequiredOptionPrompt(missingOpts, order.getLanguage());
            return order.toBuilder()
                    .contents(fixedContents)
                    .reply(reply)
                    .screen_state(order.getScreen_state())
                    .build();
        }

        return order.toBuilder().contents(fixedContents).build();
    }

    // -------------------------- JSON → DTO --------------------------

    private OrderResponseDto parsePythonPayload(String json) {
        try {
            JsonNode root = snakeMapper.readTree(json);
            String status  = root.path("intent_type").asText(null);
            String rawText = root.path("raw_text").asText(null);
            String payment = root.path("payment_method").isNull() ? null : root.path("payment_method").asText();

            List<ContentsResponseDto> contents = new ArrayList<>();
            for (JsonNode m : (ArrayNode) root.path("recognized_menus")) contents.add(toContentsDto(m));

            return OrderResponseDto.builder()
                    .preText(rawText)
                    .screen_state(status)
                    .language("KR")
                    .payment(payment)
                    .cart(Collections.emptyList())
                    .contents(contents)
                    .build();
        } catch (IOException e) {
            throw new IllegalStateException("JSON parse fail", e);
        }
    }

    // ---------------- DTO helpers ----------------

    private ContentsResponseDto toContentsDto(JsonNode m) {
        Integer menuId = m.path("menu_id").asInt();
        Integer quantity = m.path("quantity").asInt();
        String name = m.path("name").asText(null);
        String description = m.path("description").asText(null);
        Integer basePrice = m.path("base_price").asInt();
        Integer totalPrice = m.path("total_price").asInt();
        String imageUrl = m.path("image_url").asText(null);

        List<OptionsDto> options = new ArrayList<>();
        for (JsonNode o : m.path("options")) options.add(toOptionsDto(o));

        List<OptionsDto> selected = new ArrayList<>();
        for (JsonNode so : m.path("selected_options")) {
            OptionsDto dto = toOptionsDto(so);
            Integer selId = so.path("option_details").isEmpty() ? null : so.path("option_details").get(0).path("id").asInt();
            selected.add(dto.toBuilder().isSelected(true).selectedId(selId).build());
        }

        return ContentsResponseDto.builder()
                .menuId(menuId)
                .quantity(quantity)
                .name(name)
                .description(description)
                .basePrice(basePrice)
                .totalPrice(totalPrice)
                .imageUrl(imageUrl)
                .options(options)
                .selectedOption(selected)
                .build();
    }

    private OptionsDto toOptionsDto(JsonNode o) {
        Integer optionId = o.path("option_id").asInt();
        String optionName = o.path("option_name").asText(null);
        boolean required = o.path("required").asBoolean(false);
        boolean isSelected = o.path("is_selected").asBoolean(false);
        Integer selectedId = o.path("selected_id").isNull() ? null : o.path("selected_id").asInt();

        List<OptionDetailsDto> detailDtos = new ArrayList<>();
        for (JsonNode d : o.path("option_details")) {
            detailDtos.add(
                    OptionDetailsDto.builder()
                            .optionDetailId(d.path("id").asInt())
                            .optionDetailValue(d.path("value").asText())
                            .additionalPrice(d.path("additional_price").asInt())
                            .build());
        }

        return OptionsDto.builder()
                .optionId(optionId)
                .optionName(optionName)
                .required(required)
                .isSelected(isSelected)
                .selectedId(selectedId)
                .optionDetails(detailDtos)
                .build();
    }

    // ---------------- 검증 & 교정 ----------------

    private ContentsResponseDto validateAndCorrect(ContentsResponseDto content, List<String> missingOptNames) {
        menuRepository.findById(content.getMenuId())
                .orElseThrow(() -> new IllegalStateException("menu not found"));

        List<MenuOptionMap> maps = menuOptionRepository.findAllWithDetailByMenuId(content.getMenuId());
        if (maps.isEmpty()) return content;

        Map<Integer, List<MenuOptionMap>> grouped = maps.stream()
                .collect(Collectors.groupingBy(m -> m.getOptions().getId()));

        List<OptionsDto> canonical = new ArrayList<>();
        for (var entry : grouped.entrySet()) {
            Integer optionId = entry.getKey();
            List<MenuOptionMap> group = entry.getValue();

            String optionNameKr = group.get(0).getOptions().getOptionNameKr();
            boolean required = group.stream().anyMatch(MenuOptionMap::getIsRequired);

            List<OptionDetailsDto> detailDtos = group.stream()
                    .map(MenuOptionMap::getOptionDetail)
                    .map(this::toOptionDetailsDto)
                    .toList();

            Optional<OptionsDto> incoming = content.getOptions().stream()
                    .filter(o -> Objects.equals(o.getOptionId(), optionId))
                    .findFirst();

            boolean isSelected = incoming.map(OptionsDto::isSelected).orElse(false);
            Integer selectedId = incoming.map(OptionsDto::getSelectedId).orElse(null);

            if (required && !isSelected) missingOptNames.add(optionNameKr);

            canonical.add(OptionsDto.builder()
                    .optionId(optionId)
                    .optionName(optionNameKr)
                    .required(required)
                    .isSelected(isSelected)
                    .selectedId(selectedId)
                    .optionDetails(detailDtos)
                    .build());
        }

        List<OptionsDto> selectedOnly = canonical.stream()
                .filter(OptionsDto::isSelected)
                .map(o -> {
                    OptionDetailsDto sel = o.getOptionDetails().stream()
                            .filter(d -> Objects.equals(d.getOptionDetailId(), o.getSelectedId()))
                            .findFirst().orElse(null);
                    return o.toBuilder().optionDetails(sel == null ? List.of() : List.of(sel)).build();
                }).toList();

        return content.toBuilder()
                .options(canonical)
                .selectedOption(selectedOnly)
                .build();
    }

    private OptionDetailsDto toOptionDetailsDto(OptionDetail d) {
        return OptionDetailsDto.builder()
                .optionDetailId(d.getId())
                .optionDetailValue(d.getValue())
                .additionalPrice(d.getAdditionalPrice())
                .build();
    }
}
