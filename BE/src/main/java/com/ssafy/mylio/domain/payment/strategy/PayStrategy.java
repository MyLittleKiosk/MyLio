package com.ssafy.mylio.domain.payment.strategy;

import com.ssafy.mylio.domain.payment.dto.request.KakaoPayApproveRequestDto;
import com.ssafy.mylio.domain.payment.dto.request.PayRequestDto;
import com.ssafy.mylio.domain.payment.dto.response.ApproveResponseDto;
import com.ssafy.mylio.domain.payment.dto.response.ReadyResponseDto;
import com.ssafy.mylio.domain.payment.entity.PaymentMethod;
import com.ssafy.mylio.global.common.constants.PayType;
import reactor.core.publisher.Mono;

public interface PayStrategy {

    Mono<ReadyResponseDto> readyToPay(Integer userId, PayRequestDto requestDto);

    Mono<ApproveResponseDto> approveToPay(KakaoPayApproveRequestDto requestDto, Integer userId, Integer storeId);

    PaymentMethod getPaymentMethod();

}
