package com.ssafy.mylio.domain.payment.strategy;

import com.ssafy.mylio.domain.order.service.OrderService;
import com.ssafy.mylio.domain.payment.dto.request.KakaoPayApproveRequestDto;
import com.ssafy.mylio.domain.payment.dto.request.PayRequestDto;
import com.ssafy.mylio.domain.payment.dto.response.ApproveResponseDto;
import com.ssafy.mylio.domain.payment.dto.response.ReadyResponseDto;
import com.ssafy.mylio.domain.payment.entity.PaymentMethod;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

@Component
@RequiredArgsConstructor
public class CardStrategy implements PayStrategy{

    private final OrderService orderService;
    @Override
    public Mono<ReadyResponseDto> readyToPay(Integer userId, PayRequestDto requestDto) {
        return Mono.empty();
    }

    @Override
    public Mono<ApproveResponseDto> approveToPay(KakaoPayApproveRequestDto requestDto, Integer userId, Integer storeId) {

        return orderService.saveOrderAfterKakaoPay(storeId, requestDto.getCart(), getPaymentMethod())
                .then(Mono.empty());
    }

    @Override
    public PaymentMethod getPaymentMethod() {
        return PaymentMethod.CARD;
    }
}
