package com.ssafy.mylio.domain.payment.controller;

import com.ssafy.mylio.domain.payment.dto.request.PayRequestDto;
import com.ssafy.mylio.domain.payment.dto.response.ApproveResponseDto;
import com.ssafy.mylio.domain.payment.dto.response.ReadyResponseDto;
import com.ssafy.mylio.domain.payment.service.KakaoPayService;
import com.ssafy.mylio.global.common.response.CommonResponse;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import com.ssafy.mylio.global.util.AuthenticationUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/pay")
@RequiredArgsConstructor
@Tag(name = "카카오페이 결제", description = "카카오페이 결제를 진행합니다")
public class PaymentController {

    private final AuthenticationUtil authenticationUtil;
    private final KakaoPayService kakaoPayService;

    @PostMapping("/ready")
    @Operation(summary = "카카오페이 결제 요청", description = "카카오페이 결제 요청을 진행합니다(QR 요청)")
    public ResponseEntity<CommonResponse<ReadyResponseDto>> readyToPay(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestBody PayRequestDto payRequestDto) {
        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        return CommonResponse.ok(kakaoPayService.readyToPay(userId, payRequestDto).block());
    }

    @GetMapping("/success")
    @Operation(summary = "카카오페이 결제 성공", description = "카카오페이 결제 성공")
    public Mono<ResponseEntity<CommonResponse<ApproveResponseDto>>> paySuccess(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestParam("pg_token") String pgToken,
            @RequestParam("orderId") String orderId) {

        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        return kakaoPayService.approveToPay(orderId, pgToken, userId)
                .map(result -> CommonResponse.ok(result));
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
