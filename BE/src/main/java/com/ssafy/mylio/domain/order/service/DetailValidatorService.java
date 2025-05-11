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
import com.ssafy.mylio.domain.order.util.OrderJsonMapper;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
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
    private final OrderJsonMapper mapper;

    public Mono<OrderResponseDto> validate(String pyJson, UserPrincipal user) {
        return Mono.fromCallable(() -> parseAndValidate(mapper.parse(pyJson, user), user))
                .subscribeOn(Schedulers.boundedElastic());
    }

    @Transactional(readOnly = true)
    protected OrderResponseDto parseAndValidate(OrderResponseDto order, UserPrincipal user) {
        List<ContentsResponseDto> fixed = order.getContents().stream()
                .map(this::syncNutritionInfo)
                .toList();

        return order.toBuilder().contents(fixed).build();
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
