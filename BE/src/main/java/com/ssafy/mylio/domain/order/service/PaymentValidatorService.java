package com.ssafy.mylio.domain.order.service;

import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import com.ssafy.mylio.domain.order.util.OrderJsonMapper;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

@Service
@Slf4j
@RequiredArgsConstructor
public class PaymentValidatorService {

    private final OrderJsonMapper mapper;

    public Mono<OrderResponseDto> validate(String pyJson) {
        log.info("결제 검증 로직 진입 : {}", pyJson);
        return Mono.fromCallable(() -> parseAndValidate(mapper.parse(pyJson)))
                .subscribeOn(Schedulers.boundedElastic());
    }

    // 결제 검증 로직
    protected OrderResponseDto parseAndValidate(OrderResponseDto order) {

        if (order.getScreenState().equals("CONFIRM") && order.getCart().isEmpty())
            throw new CustomException(ErrorCode.MENU_NOT_FOUND, "장바구니가 비어 있습니다.");

        return order;
    }
}
