package com.ssafy.mylio.domain.payment.controller;

import com.ssafy.mylio.domain.payment.dto.request.KakaoPayApproveRequestDto;
import com.ssafy.mylio.domain.payment.dto.request.PayRequestDto;
import com.ssafy.mylio.domain.payment.dto.response.ApproveResponseDto;
import com.ssafy.mylio.domain.payment.dto.response.ReadyResponseDto;
import com.ssafy.mylio.domain.payment.entity.PaymentMethod;
import com.ssafy.mylio.domain.payment.service.PaymentService;
import com.ssafy.mylio.global.common.response.CommonResponse;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import com.ssafy.mylio.global.util.AuthenticationUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/pay")
@RequiredArgsConstructor
@Tag(name = "카카오페이 결제", description = "카카오페이 결제를 진행합니다")
@Slf4j
public class PaymentController {

    private final AuthenticationUtil authenticationUtil;
    private final PaymentService paymentService;

    @PostMapping("/ready")
    public ResponseEntity<CommonResponse<ReadyResponseDto>> readyToPay(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestBody PayRequestDto payRequestDto,
            @RequestParam("pay_method") String payMethod
        ) {

        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        ReadyResponseDto response = paymentService.readyToPay(userId, payRequestDto, PaymentMethod.fromCode(payMethod)).block();
        return CommonResponse.ok(response);
    }

    @PostMapping("/success")
    @Operation(summary = "카카오페이 결제 성공", description = "카카오페이 결제 성공")
    public ResponseEntity<CommonResponse<ApproveResponseDto>> paySuccess(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestBody KakaoPayApproveRequestDto kakaoDto,
            @RequestParam("pay_method") String payMethod
    ) {

        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);

        ApproveResponseDto response = paymentService.approveToPay(kakaoDto, userId, storeId, PaymentMethod.fromCode(payMethod)).block();
        return CommonResponse.ok(response);
    }

    @GetMapping("/cancel")
    @Operation(summary = "카카오페이 결제 취소", description = "카카오페이 결제 취소")
    public ResponseEntity<CommonResponse<Object>> cancel() {
        return CommonResponse.error(ErrorCode.PAY_CANCEL);
    }

    @GetMapping("/fail")
    @Operation(summary = "카카오페이 결제 실패", description = "카카오페이 결제 실패")
    public ResponseEntity<CommonResponse<Object>> fail(){
        return CommonResponse.error(ErrorCode.PAY_FAIL);
    }

}
