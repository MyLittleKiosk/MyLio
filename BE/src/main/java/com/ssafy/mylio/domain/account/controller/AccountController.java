package com.ssafy.mylio.domain.account.controller;

import com.ssafy.mylio.domain.account.dto.request.AccountCreateRequest;
import com.ssafy.mylio.domain.account.dto.request.AccountModifyRequestDto;
import com.ssafy.mylio.domain.account.dto.request.PasswordRequestDto;
import com.ssafy.mylio.domain.account.dto.response.AccountDetailResponseDto;
import com.ssafy.mylio.domain.account.dto.response.AccountGetInfoResponseDto;
import com.ssafy.mylio.domain.account.dto.response.AccountListResponseDto;
import com.ssafy.mylio.domain.account.dto.response.AccountModifyResponse;
import com.ssafy.mylio.domain.account.service.AccountService;
import com.ssafy.mylio.global.aop.swagger.ApiErrorCodeExamples;
import com.ssafy.mylio.global.common.CustomPage;
import com.ssafy.mylio.global.common.response.CommonResponse;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import com.ssafy.mylio.global.util.AuthenticationUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;
import com.ssafy.mylio.domain.account.dto.request.ModifyPasswordRequest;

@RestController
@RequestMapping("/account")
@RequiredArgsConstructor
@Tag(name = "계정", description = "계정 관리 API")
public class AccountController {
    private final AuthenticationUtil authenticationUtil;
    private final AccountService accountService;

    @PostMapping
    @Operation(summary = "매장 관리자 계정 생성",description = "매장 관리자 계정을 생성합니다.")
    @ApiErrorCodeExamples({ErrorCode.EMAIL_ALREADY_EXISTS,ErrorCode.INVALID_ROLE,ErrorCode.STORE_NOT_FOUND,ErrorCode.STORE_NOT_FOUND})
    public ResponseEntity<CommonResponse<Void>> createAccount(
            @Valid @RequestBody AccountCreateRequest request,
            @AuthenticationPrincipal UserPrincipal userPrincipal) {
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        accountService.createAccount(userType, request);
        return CommonResponse.ok();

    }

    @PatchMapping
    @Operation(summary = "매장 관리자 계정 수정", description = "매장 관리자 계정을 수정합니다.")
    @ApiErrorCodeExamples({ErrorCode.INVALID_ROLE,ErrorCode.ACOUNT_NOT_FOUND,ErrorCode.STORE_NOT_FOUND})
    public ResponseEntity<CommonResponse<AccountModifyResponse>> modifyAccount(
            @Valid @RequestBody AccountModifyRequestDto request,
            @AuthenticationPrincipal UserPrincipal userPrincipal
    ){
        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        return CommonResponse.ok(accountService.modifyAccount(userId,storeId,userType,request));
    }

    @DeleteMapping("{accountId}")
    @Operation(summary = "매장 관리자 계정 삭제", description = "매장 관리자 계정을 삭제합니다.\n\n매장관리자 id를 보내줘야합니다.")
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND,ErrorCode.ACOUNT_NOT_FOUND,ErrorCode.INVALID_ROLE})
    public ResponseEntity<CommonResponse<Void>> deleteAccount(
            @PathVariable("accountId") Integer accountId,
            @AuthenticationPrincipal UserPrincipal userPrincipal
    ) {
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        accountService.deleteAccount(accountId, userType);
        return CommonResponse.ok();
    }

    @PatchMapping("/pw")
    @Operation(summary = "매장 관리자 비밀번호 재발급")
    @ApiErrorCodeExamples({ErrorCode.FORBIDDEN_AUTH,ErrorCode.ACOUNT_NOT_FOUND})
    public ResponseEntity<CommonResponse<String>> findPassword(
            @Valid @RequestBody PasswordRequestDto request
    ){
        return CommonResponse.ok(accountService.findPassword(request));
    }

    @GetMapping
    @Operation(summary ="계정 전체 및 검색 조회", description = "사용자 이름, 이메일, 매장 이름으로 검색합니다.")
    @ApiErrorCodeExamples({ErrorCode.INVALID_ROLE})
    public ResponseEntity<CommonResponse<CustomPage<AccountListResponseDto>>> getAccessList(
            @RequestParam(required = false) String keyword,
            @PageableDefault(size = 10, page = 0,sort = "username", direction  = Sort.Direction.ASC) Pageable pageable,
            @AuthenticationPrincipal UserPrincipal userPrincipal) {

        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        return CommonResponse.ok(accountService.getAccountList(userType, keyword, pageable));
    }

    @GetMapping("/detail")
    @Operation(summary = "계정 상세 조회" , description = "매장 관리자가 본인의 계정정보를 확인합니다.")
    @ApiErrorCodeExamples({ErrorCode.INVALID_ROLE,ErrorCode.INVALID_ROLE,ErrorCode.STORE_NOT_FOUND})
    public ResponseEntity<CommonResponse<AccountDetailResponseDto>> getAccountDetail(
            @AuthenticationPrincipal UserPrincipal userPrincipal){

        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);

        return CommonResponse.ok(accountService.getAccountDetail(userId,storeId,userType));
    }

    @PatchMapping("/change_pw")
    @Operation(summary = "비밀번호 수정", description = "매장관리자가 본인의 비밀번호를 수정합니디.")
    @ApiErrorCodeExamples({ErrorCode.ACOUNT_NOT_FOUND,ErrorCode.FORBIDDEN_AUTH})
    public ResponseEntity<CommonResponse<Void>> modifyPassword(
            @Valid @RequestBody ModifyPasswordRequest request,
            @AuthenticationPrincipal UserPrincipal userPrincipal){
        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);

        accountService.modifyPW(userId,userType,request);
        return CommonResponse.ok();
    }

    @GetMapping("/role")
    @Operation(summary = "계정 정보 조회", description = "모든 계정의 정보를 조회합니다.")
    @ApiErrorCodeExamples({})
    public ResponseEntity<CommonResponse<AccountGetInfoResponseDto>> getAccountInfo(
            @AuthenticationPrincipal UserPrincipal userPrincipal){
        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        return CommonResponse.ok(accountService.getAcountInfo(userId,userType));
    }
}
