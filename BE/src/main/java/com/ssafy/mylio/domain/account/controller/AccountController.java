package com.ssafy.mylio.domain.account.controller;

import com.ssafy.mylio.domain.account.dto.request.AccountCreateRequest;
import com.ssafy.mylio.domain.account.dto.request.AccountModifyRequestDto;
import com.ssafy.mylio.domain.account.dto.response.AccountModifyResponse;
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
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/account")
@RequiredArgsConstructor
@Tag(name = "계정", description = "계정 관리 API")
public class AccountController {
    private final AuthenticationUtil authenticationUtil;
    private final AccountService accountService;

    @PostMapping
    @Operation(summary = "관리자 계정 생성", description = "관리자 계정을 생성합니다.")
    @ApiErrorCodeExamples({ErrorCode.INVALID_ROLE, ErrorCode.STORE_NOT_FOUND, ErrorCode.STORE_NOT_FOUND})
    public ResponseEntity<CommonResponse<Void>> createAccount(
            @Valid @RequestBody AccountCreateRequest request,
            @AuthenticationPrincipal UserPrincipal userPrincipal) {
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        accountService.createAccount(userType, request);
        return CommonResponse.ok();

    }

    @PatchMapping
    @Operation(summary = "관리자 계정 수정", description = "관리자 계정을 수정합니다.")
    @ApiErrorCodeExamples({ErrorCode.INVALID_ROLE, ErrorCode.ACOUNT_NOT_FOUND})
    public ResponseEntity<CommonResponse<AccountModifyResponse>> modifyAccount(
            @Valid @RequestBody AccountModifyRequestDto request,
            @AuthenticationPrincipal UserPrincipal userPrincipal
    ) {
        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        return CommonResponse.ok(accountService.modifyAccount(userId, userType, request));
    }

    @DeleteMapping("{account_id}")
    @Operation(summary = "매장 관리자 계정 삭제", description = "매장 관리자 계정을 삭제합니다.\n\n매장관리자 id를 보내줘야합니다.")
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND,ErrorCode.ACOUNT_NOT_FOUND,ErrorCode.INVALID_ROLE})
    public ResponseEntity<CommonResponse<Void>> deleteAccount(
            @PathVariable("account_id") Integer accountId,
            @AuthenticationPrincipal UserPrincipal userPrincipal
    ) {
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        accountService.deleteAccount(accountId, userType);
        return CommonResponse.ok();
    }

}
