package com.ssafy.mylio.domain.account.controller;

import com.ssafy.mylio.domain.account.dto.request.AccountCreateRequest;
import com.ssafy.mylio.domain.account.dto.response.AccountCreateResponseDto;
import com.ssafy.mylio.domain.account.service.AccountService;
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
@RequestMapping("/account")
@RequiredArgsConstructor
@Tag(name = "계정", description = "계정 관리 API")
public class AccountController {
    private final AuthenticationUtil authenticationUtil;
    private final AccountService accountService;

    @PostMapping("")
    @Operation(summary = "관리자 계정 생성",description = "관리자 계정을 생성합니다.")
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND,ErrorCode.INVALID_ROLE})
    public ResponseEntity<CommonResponse<AccountCreateResponseDto>> createAccount(
            @Valid @RequestBody AccountCreateRequest request,
            @AuthenticationPrincipal UserPrincipal userPrincipal){
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        return CommonResponse.ok(accountService.createAccount(userType,request));

    }
}
