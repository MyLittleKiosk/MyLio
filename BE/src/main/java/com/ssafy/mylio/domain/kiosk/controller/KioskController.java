package com.ssafy.mylio.domain.kiosk.controller;

import com.ssafy.mylio.domain.kiosk.dto.request.KioskCreateRequestDto;
import com.ssafy.mylio.domain.kiosk.dto.response.KioskCreateResponseDto;
import com.ssafy.mylio.domain.kiosk.service.KioskService;
import com.ssafy.mylio.global.aop.swagger.ApiErrorCodeExamples;
import com.ssafy.mylio.global.common.response.CommonResponse;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import com.ssafy.mylio.global.util.AuthenticationUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/kiosk")
@RequiredArgsConstructor
@Tag(name = "키오스크", description="키오스크 관리 API")
public class KioskController {
    private final AuthenticationUtil authenticationUtil;
    private final KioskService kioskService;

    @PostMapping()
    @Operation(summary = "키오스크 등록", description = "매장 관리자가 키오스크를 등록합니다.")
    @ApiErrorCodeExamples({ErrorCode.INVALID_ROLE,ErrorCode.ACOUNT_NOT_FOUND,ErrorCode.STORE_NOT_FOUND,ErrorCode.ALREADY_EXIST_KIOSK})
    public ResponseEntity<CommonResponse<KioskCreateResponseDto>> createKiosk(
            @Valid @RequestBody KioskCreateRequestDto request,
            @AuthenticationPrincipal UserPrincipal userPrincipal){

        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);

        return CommonResponse.ok(kioskService.createKiosk(userId,userType,storeId,request));
    }

}
