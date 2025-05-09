package com.ssafy.mylio.domain.order.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.ssafy.mylio.domain.nutrition.entity.NutritionValue;
import com.ssafy.mylio.domain.nutrition.repository.NutritionRepository;
import com.ssafy.mylio.domain.order.dto.common.NutritionInfoDto;
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
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class DetailValidatorService {

    private final NutritionRepository nutritionRepository;
    private final ObjectMapper snakeMapper = new ObjectMapper()
            .setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE);

    public Mono<OrderResponseDto> validate(String pyJson){
        return Mono.fromCallable(() -> parseAndValidate(pyJson))
                .subscribeOn(Schedulers.boundedElastic());
    }

    @Transactional(readOnly = true)
    protected OrderResponseDto parseAndValidate(String json) {
        OrderResponseDto order = parsePythonPayload(json);

        List<ContentsResponseDto> fixed = order.getContents().stream()
                .map(this::syncNutritionInfo)
                .toList();

        return order.toBuilder().contents(fixed).build();
    }

    // JSON 파싱
    private OrderResponseDto parsePythonPayload(String json) {
        try {
            JsonNode root = snakeMapper.readTree(json);
            JsonNode data = root.path("data");

            // root 노드 값 파싱
            String status  = root.path("screen_state").asText(null);
            String payment = root.path("payment_method").isNull() ? null : root.path("payment_method").asText();

            // data 값 파싱
            String preText = data.path("pre_text").asText(null);
            String postText = data.path("post_text").asText(null);
            String reply = data.path("reply").asText(null);
            String sessionId = data.path("session_id").asText(null);


            List<ContentsResponseDto> contents = new ArrayList<>();
            for (JsonNode m : (ArrayNode) root.path("contents")) {
                Integer menuId = m.path("menu_id").asInt();
                Integer quantity = m.path("quantity").asInt();
                String name = m.path("name").asText();
                Integer basePrice = m.path("base_price").asInt();
                Integer totalPrice = m.path("total_price").asInt();

                contents.add(ContentsResponseDto.builder()
                        .menuId(menuId)
                        .quantity(quantity)
                        .name(name)
                        .basePrice(basePrice)
                        .totalPrice(totalPrice)
                        .nutritionInfo(Collections.emptyList()) // placeholder
                        .build());
            }

            return OrderResponseDto.builder()
                    .preText(preText)
                    .postText(postText)
                    .reply(reply)
                    .screenState(status)
                    .language("KR")
                    .sessionId(sessionId)
                    .payment(payment)
                    .cart(Collections.emptyList())
                    .contents(contents)
                    .build();

        } catch (IOException e) {
            throw new CustomException(ErrorCode.INTERNAL_SERVER_ERROR, "jsonParserError");
        }
    }

    private ContentsResponseDto syncNutritionInfo(ContentsResponseDto content) {
        List<NutritionValue> values = nutritionRepository.findAllWithTemplateByMenuId(content.getMenuId());

        List<NutritionInfoDto> Dtos = values.stream()
                .map(v -> NutritionInfoDto.builder()
                        .nutritionId(v.getNutrition().getId())
                        .nutritionName(v.getNutrition().getNameKr())
                        .nutritionValue(v.getValue().intValue())
                        .nutritionType(v.getNutrition().getUnitType())
                        .build()
                ).toList();

        // 비교: 갯수와 각 nutritionId & value 일치 여부
        boolean identical = Optional.ofNullable(content.getNutritionInfo())
                .filter(list -> list.size() == Dtos.size())
                .map(Dtos::containsAll)
                .orElse(false);

        if (identical) return content; // 그대로 반환

        return content.toBuilder().nutritionInfo(Dtos).build();
    }
}
