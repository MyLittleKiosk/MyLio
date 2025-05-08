package com.ssafy.mylio.domain.order.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
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
    private final MenuOptionRepository menuOptionMapRepository;
    private final ObjectMapper objectMapper;

    /**
     * FastAPI에서 넘겨준 JSON → OrderResponseDto 변환 → 옵션 검증·교정
     *
     * @param pyJson FastAPI에서 넘겨준 JSON 문자열
     * @return OrderResponseDto
     */
    public Mono<OrderResponseDto> validate(String pyJson) {
        return Mono.fromCallable(() -> {
            OrderResponseDto order = parsePythonPayload(pyJson);

            // 옵션 검증 & DB 기준 교정
            List<ContentsResponseDto> correctedContents = order.getContents().stream()
                    .map(this::validateAndCorrect)
                    .toList();

            return order.toBuilder().contents(correctedContents).build();
        }).subscribeOn(Schedulers.boundedElastic());
    }

    // 옵션 검증
    private ContentsResponseDto validateAndCorrect(ContentsResponseDto content) {
        // 1. 메뉴 존재 확인
        Menu menu = menuRepository.findById(content.getMenuId())
                .orElseThrow(() -> new CustomException(ErrorCode.MENU_NOT_FOUND, "menuId", content.getMenuId()));

        // 2. 메뉴-옵션 매핑 조회
        List<MenuOptionMap> mappingList = menuOptionMapRepository.findAllByMenuId(content.getMenuId());
        if (mappingList.isEmpty()) return content; // 옵션 자체가 없는 메뉴

        // 2-1. OptionId 별로 묶어서 “정해진 옵션 목록” 구축
        // key : option_id, value : 동일 option_id에 대한 MenuOptionMap 목록
        Map<Integer, List<MenuOptionMap>> byOptionId = mappingList.stream()
                .collect(Collectors.groupingBy(m -> m.getOptions().getId()));

        // 최종적으로 DB 기준으로 만든 옵션 목록
        List<OptionsDto> canonicalOptions = new ArrayList<>();

        // option_id 별 그룹을 순회하며 canonical 옵션을 만든다
        for (Map.Entry<Integer, List<MenuOptionMap>> entry : byOptionId.entrySet()) {
            Integer optionId = entry.getKey();              // ex) 101(온도)
            List<MenuOptionMap> optionMaps = entry.getValue(); // 그 option_id에 대한 모든 레코드

            // 옵션 자체의 메타데이터(한글명, 영문명 등)는 아무 레코드나 꺼내면 동일
            Options optionEntity = optionMaps.get(0).getOptions();

            // is_required 중 하나라도 true면 “필수 옵션”
            boolean required = optionMaps.stream()
                    .anyMatch(MenuOptionMap::getIsRequired);

            // ---------- DB 기준 option_detail 목록을 OptionDetailsDto 로 변환 ----------
            List<OptionDetailsDto> detailDtoList = optionMaps.stream()
                    .map(MenuOptionMap::getOptionDetail)   // OptionDetail 엔티티
                    .map(this::toOptionDetailsDto)         // → OptionDetailsDto
                    .toList();

            // ---------- 파이썬쪽 옵션과 비교 ----------
            // content.getOptions() 에서 동일 optionId를 가진 요소를 찾음
            Optional<OptionsDto> incomingOpt = Optional.ofNullable(content.getOptions())
                    .orElse(Collections.emptyList())
                    .stream()
                    .filter(o -> Objects.equals(o.getOptionId(), optionId))
                    .findFirst();

            // 요청에 optionId가 아예 없으면 isSelected=false, selectedId=null
            boolean isSelected = incomingOpt.map(OptionsDto::isSelected).orElse(false);
            Integer selectedId = incomingOpt.map(OptionsDto::getSelectedId).orElse(null);

            // ---------- 3. 필수 옵션인데 선택되지 않았으면 예외 ----------
            if (required && !isSelected) {
                throw new CustomException(ErrorCode.REQUIRED_OPTION_MISSING, "optionId", optionId);
            }

            // ---------- 4. canonical 옵션(DTO) 생성 ----------
            canonicalOptions.add(
                    OptionsDto.builder()
                            .optionId(optionId)
                            .optionName(optionEntity.getOptionNameKr()) // ex) "온도"
                            .required(required)
                            .isSelected(isSelected)
                            .selectedId(selectedId)             // null 가능
                            .optionDetails(detailDtoList)       // DB 기준 detail 전체
                            .build()
            );
        }

        // ---- selectedOption(교정된) 생성: canonicalOptions 중 선택된 것만 ----
        List<OptionsDto> canonicalSelected = canonicalOptions.stream()
                .filter(OptionsDto::isSelected)
                .map(o -> {
                    // 선택된 detail 하나만 남기기
                    OptionDetailsDto selDetail = o.getOptionDetails().stream()
                            .filter(d -> Objects.equals(d.getOptionDetailId(), o.getSelectedId()))
                            .findFirst()
                            .orElse(null);
                    return o.toBuilder()
                            .optionDetails(selDetail == null ? List.of() : List.of(selDetail))
                            .build();
                })
                .toList();

        // ------------------ 5. 교정된 옵션을 덮어써서 반환 ------------------
        return content.toBuilder()
                .options(canonicalOptions)
                .selectedOption(canonicalSelected)
                .build();
    }



    // JSON과 DTO 매핑
    private OrderResponseDto parsePythonPayload(String json) {
        try {
            JsonNode root = objectMapper.readTree(json);

            // status, text, payment 등 매핑
            String status = root.path("screen_state").asText(null);
            String rawText = root.path("raw_text").asText(null);
            String payment = root.path("payment_method").isNull() ? null : root.path("payment_method").asText();

            List<ContentsResponseDto> contents = new ArrayList<>();
            ArrayNode menusNode = (ArrayNode) root.path("recognized_menus");
            for (JsonNode m : menusNode) {
                contents.add(toContentsDto(m));
            }

            return OrderResponseDto.builder()
                    .preText(rawText)
                    .postText(null)
                    .reply(null)
                    .status(status)
                    .language("KR")
                    .sessionId(null)
                    .payment(payment)
                    .cart(Collections.emptyList())
                    .contents(contents)
                    .build();
        } catch (IOException e) {
            log.error("[OrderValidator] JSON 파싱 실패", e);
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

        // options 전체
        List<OptionsDto> options = new ArrayList<>();
        for (JsonNode o : m.path("options")) {
            options.add(toOptionsDto(o));
        }

        // 선택된 옵션만
        List<OptionsDto> selectedOptions = new ArrayList<>();
        for (JsonNode so : m.path("selected_options")) {
            // selected_options 구조엔 selected_id 가 없고 option_details 하나만 들어옴
            OptionsDto dto = toOptionsDto(so);
            // selected_id는 option_details[0].id 로 유추
            Integer selId = so.path("option_details").isEmpty() ? null : so.path("option_details").get(0).path("id").asInt();
            dto = dto.toBuilder().isSelected(true).selectedId(selId).build();
            selectedOptions.add(dto);
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
                .selectedOption(selectedOptions)
                .nutritionInfo(null)
                .build();
    }

    private OptionsDto toOptionsDto(JsonNode o) {
        Integer optionId = o.path("option_id").asInt();
        String optionName = o.path("option_name").asText(null);
        boolean required = o.path("required").asBoolean(false);
        boolean isSelected = o.path("is_selected").asBoolean(false);
        Integer selectedId = o.path("selected_id").isNull() ? null : o.path("selected_id").asInt();

        List<OptionDetailsDto> detailDtoList = new ArrayList<>();
        for (JsonNode d : o.path("option_details")) {
            detailDtoList.add(OptionDetailsDto.builder()
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
                .optionDetails(detailDtoList)
                .build();
    }

    private OptionDetailsDto toOptionDetailsDto(OptionDetail detail) {
        return OptionDetailsDto.builder()
                .optionDetailId(detail.getId())
                .optionDetailValue(detail.getValue())
                .additionalPrice(detail.getAdditionalPrice())
                .build();
    }
}
