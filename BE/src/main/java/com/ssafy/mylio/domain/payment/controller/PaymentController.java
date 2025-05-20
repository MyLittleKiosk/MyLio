package com.ssafy.mylio.domain.payment.controller;

import com.ssafy.mylio.domain.payment.dto.request.KakaoPayApproveRequestDto;
import com.ssafy.mylio.domain.payment.dto.request.PayRequestDto;
import com.ssafy.mylio.domain.payment.dto.response.ApproveResponseDto;
import com.ssafy.mylio.domain.payment.dto.response.ReadyResponseDto;
import com.ssafy.mylio.domain.payment.entity.PaymentMethod;
import com.ssafy.mylio.domain.payment.service.PayService;
import com.ssafy.mylio.domain.payment.service.PaymentFacadeService;
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
    private final PaymentFacadeService paymentFacadeService;


    @PostMapping("/ready")
    public ResponseEntity<CommonResponse<ReadyResponseDto>> readyToPay(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestBody PayRequestDto payRequestDto) {

        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);

        // 리액티브하게 서비스를 찾습니다
        PayService service = paymentFacadeService.resolve(PaymentMethod.PAY).block();

        // 찾은 서비스로 결제 준비를 시작합니다
        ReadyResponseDto response = service.readyToPay(userId, payRequestDto).block();

        return CommonResponse.ok(response);
    }

    @PostMapping("/success")
    @Operation(summary = "카카오페이 결제 성공", description = "카카오페이 결제 성공")
    public ResponseEntity<CommonResponse<ApproveResponseDto>> paySuccess(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestBody KakaoPayApproveRequestDto kakaoDto) {

        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);

        // 리액티브 서비스 조회 후 block
        PayService service = paymentFacadeService.resolve(PaymentMethod.PAY).block();

        // 결제 승인 처리 후 block
        ApproveResponseDto response = service.approveToPay(kakaoDto, userId, storeId).block();
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
