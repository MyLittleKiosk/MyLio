package com.ssafy.mylio.domain.payment.service;

import com.ssafy.mylio.domain.payment.dto.request.KakaoPayApproveRequestDto;
import com.ssafy.mylio.domain.payment.dto.request.PayRequestDto;
import com.ssafy.mylio.domain.payment.dto.response.ApproveResponseDto;
import com.ssafy.mylio.domain.payment.dto.response.ReadyResponseDto;
import com.ssafy.mylio.domain.payment.entity.PaymentMethod;
import reactor.core.publisher.Mono;

public interface PayService {
    Mono<ReadyResponseDto> readyToPay(Integer userId, PayRequestDto requestDto);

    Mono<ApproveResponseDto> approveToPay(KakaoPayApproveRequestDto requestDto, Integer userId, Integer storeId);

    PaymentMethod getPaymentMethod();
}
