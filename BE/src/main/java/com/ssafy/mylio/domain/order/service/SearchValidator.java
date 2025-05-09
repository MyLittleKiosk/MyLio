package com.ssafy.mylio.domain.order.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.ssafy.mylio.domain.order.dto.common.OptionDetailsDto;
import com.ssafy.mylio.domain.order.dto.common.OptionsDto;
import com.ssafy.mylio.domain.order.dto.response.CartResponseDto;
import com.ssafy.mylio.domain.order.dto.response.ContentsResponseDto;
import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import com.ssafy.mylio.domain.order.util.OrderJsonMapper;
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
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class SearchValidator {

    private final OrderJsonMapper mapper;

    public Mono<OrderResponseDto> validate(String pyJson) {
        log.info("옵션 검증 로직 진입 : {}", pyJson);
        return Mono.fromCallable(() -> parseAndValidate(mapper.parse(pyJson)))
                .subscribeOn(Schedulers.boundedElastic());
    }

    @Transactional(readOnly = true)
    protected OrderResponseDto parseAndValidate(OrderResponseDto order) {
        // 여기에 검색 결과 검증 로직

        return order.toBuilder().build();
    }
}
