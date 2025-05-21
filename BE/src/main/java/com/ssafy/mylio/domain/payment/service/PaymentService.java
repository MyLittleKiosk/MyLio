package com.ssafy.mylio.domain.payment.service;

import com.ssafy.mylio.domain.payment.dto.request.KakaoPayApproveRequestDto;
import com.ssafy.mylio.domain.payment.dto.request.PayRequestDto;
import com.ssafy.mylio.domain.payment.dto.response.ApproveResponseDto;
import com.ssafy.mylio.domain.payment.dto.response.ReadyResponseDto;
import com.ssafy.mylio.domain.payment.entity.PaymentMethod;
import com.ssafy.mylio.domain.payment.strategy.PayStrategy;
import com.ssafy.mylio.domain.payment.strategy.PaymenyFactory;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;


@Service
@RequiredArgsConstructor
public class PaymentService {

    private final PaymenyFactory paymenyFactory;

    public Mono<ReadyResponseDto> readyToPay(Integer userId, PayRequestDto payRequestDto, PaymentMethod paymentMethod) {

        PayStrategy strategy = paymenyFactory.of(paymentMethod);

        return strategy.readyToPay(userId, payRequestDto);
    }
    public Mono<ApproveResponseDto> approveToPay(KakaoPayApproveRequestDto dto, Integer userId, Integer storeId, PaymentMethod paymentMethod){

        PayStrategy strategy = paymenyFactory.of(paymentMethod);

        return strategy.approveToPay(dto, userId, storeId);
    }
}
