package com.ssafy.mylio.domain.order.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.menu.repository.MenuRepository;
import com.ssafy.mylio.domain.options.entity.MenuOptionMap;
import com.ssafy.mylio.domain.options.entity.OptionDetail;
import com.ssafy.mylio.domain.options.entity.Options;
import com.ssafy.mylio.domain.options.repository.MenuOptionRepository;
import com.ssafy.mylio.domain.order.dto.common.OptionDetailsDto;
import com.ssafy.mylio.domain.order.dto.common.OptionsDto;
import com.ssafy.mylio.domain.order.dto.response.ContentsResponseDto;
import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

/**
 * OrderValidator
 * -----------------
 * ● 파이썬 JSON → OrderResponseDto 매핑
 * ● DB 옵션 정합성 검증 + 필수 옵션 체크
 * ● LazyInitializationException 방지를 위해 ★단일 트랜잭션★ 안에서
 *   모든 JPA 엔티티를 DTO 로 변환한다.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class OrderValidatorTest {

    private final MenuRepository menuRepository;
    private final MenuOptionRepository menuOptionMapRepository;

    private final ObjectMapper snakeMapper = new ObjectMapper()
            .setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE);

    /**
     * 리액티브 진입점. JPA 블로킹 코드는 boundedElastic 스케줄러로 오프로드.
     */
    public Mono<OrderResponseDto> validate(String pyJson) {
        return Mono.fromCallable(() -> parseAndValidate(pyJson))
                .subscribeOn(Schedulers.boundedElastic());
    }

    // ------------------------------------------------------------
    //  ↓↓↓  JPA 트랜잭션 경계  ↓↓↓
    // ------------------------------------------------------------

    @Transactional(readOnly = true)
    protected OrderResponseDto parseAndValidate(String json) {
        OrderResponseDto order = parsePythonPayload(json);

        List<ContentsResponseDto> corrected = order.getContents().stream()
                .map(this::validateAndCorrect)   // still inside same Tx/session
                .toList();

        return order.toBuilder().contents(corrected).build();
    }

    // -------------------------- JSON → DTO --------------------------

    private OrderResponseDto parsePythonPayload(String json) {
        try {
            JsonNode root = snakeMapper.readTree(json);
            String status  = root.path("intent_type").asText(null);
            String rawText = root.path("raw_text").asText(null);
            String payment = root.path("payment_method").isNull() ? null : root.path("payment_method").asText();

            List<ContentsResponseDto> contents = new ArrayList<>();
            for (JsonNode m : (ArrayNode) root.path("recognized_menus")) {
                contents.add(toContentsDto(m));
            }

            return OrderResponseDto.builder()
                    .preText(rawText)
                    .screen_state(status)
                    .language("KR")
                    .payment(payment)
                    .cart(Collections.emptyList())
                    .contents(contents)
                    .build();
        } catch (IOException e) {
            throw new CustomException(ErrorCode.INTERNAL_SERVER_ERROR, "payload", "order-json");
        }
    }

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
            detailDtos.add(OptionDetailsDto.builder()
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

    // ---------------- DB Canonical 검증 & 교정 ----------------

    private ContentsResponseDto validateAndCorrect(ContentsResponseDto content) {
        // 1. 메뉴 검사
        menuRepository.findById(content.getMenuId())
                .orElseThrow(() -> new CustomException(ErrorCode.MENU_NOT_FOUND, "menuId", content.getMenuId()));

        // 2. 옵션 매핑 – fetch join 메서드 사용하여 Lazy 문제 차단
        List<MenuOptionMap> maps = menuOptionMapRepository.findAllWithDetailByMenuId(content.getMenuId());
        if (maps.isEmpty()) return content;

        Map<Integer, List<MenuOptionMap>> grouped = maps.stream()
                .collect(Collectors.groupingBy(m -> m.getOptions().getId()));

        List<OptionsDto> canonical = new ArrayList<>();
        for (var entry : grouped.entrySet()) {
            Integer optionId = entry.getKey();
            List<MenuOptionMap> group = entry.getValue();

            Options option = group.get(0).getOptions();
            boolean required = group.stream().anyMatch(MenuOptionMap::getIsRequired);

            List<OptionDetailsDto> detailDtos = group.stream()
                    .map(MenuOptionMap::getOptionDetail)  // already initialized (fetch join)
                    .map(this::toOptionDetailsDto)
                    .toList();

            Optional<OptionsDto> incoming = content.getOptions().stream()
                    .filter(o -> Objects.equals(o.getOptionId(), optionId))
                    .findFirst();

            boolean isSelected = incoming.map(OptionsDto::isSelected).orElse(false);
            Integer selectedId = incoming.map(OptionsDto::getSelectedId).orElse(null);

            // 옵션 충족되었는지 검사
            if (required && !isSelected) {
                throw new CustomException(ErrorCode.REQUIRED_OPTION_MISSING, "optionId", optionId);
            }

            canonical.add(OptionsDto.builder()
                    .optionId(optionId)
                    .optionName(option.getOptionNameKr())
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
                            .findFirst()
                            .orElse(null);
                    return o.toBuilder()
                            .optionDetails(sel == null ? List.of() : List.of(sel))
                            .build();
                })
                .toList();

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
