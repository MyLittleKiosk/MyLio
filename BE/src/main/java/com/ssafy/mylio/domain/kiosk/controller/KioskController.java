package com.ssafy.mylio.domain.kiosk.controller;

import com.ssafy.mylio.domain.kiosk.dto.request.KioskCreateRequestDto;
import com.ssafy.mylio.domain.kiosk.dto.response.KioskResponseDto;
import com.ssafy.mylio.domain.kiosk.service.KioskService;
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
    public ResponseEntity<CommonResponse<KioskResponseDto>> createKiosk(
            @Valid @RequestBody KioskCreateRequestDto request,
            @AuthenticationPrincipal UserPrincipal userPrincipal){

        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);

        return CommonResponse.ok(kioskService.createKiosk(userId,userType,storeId,request));
    }

    @DeleteMapping("/{kiosk_id}")
    @Operation(summary = "키오스크 삭제", description = "매장 관리자가 키오스크를 삭제합니다.")
    @ApiErrorCodeExamples({ErrorCode.INVALID_ROLE,ErrorCode.STORE_NOT_FOUND,ErrorCode.KIOSK_NOT_FOUND})
    public ResponseEntity<CommonResponse<Void>> deleteKiosk(
            @PathVariable("kiosk_id") Integer kioskId,
            @AuthenticationPrincipal UserPrincipal userPrincipal){
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);

        kioskService.deleteKiosk(kioskId,storeId,userType);

        return CommonResponse.ok();
    }

    @PatchMapping("/{kiosk_id}")
    @Operation(summary = "키오스크 수정", description = "매장 관리자가 키오스크를 수정합니다.")
    @ApiErrorCodeExamples({ErrorCode.INVALID_ROLE,ErrorCode.STORE_NOT_FOUND,ErrorCode.KIOSK_NOT_FOUND})
    public ResponseEntity<CommonResponse<KioskResponseDto>> modifyKiosk(
            @PathVariable("kiosk_id") Integer kioskId,
            @Valid @RequestBody KioskCreateRequestDto request,
            @AuthenticationPrincipal UserPrincipal userPrincipal){
        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);

        return CommonResponse.ok(kioskService.modifyKiosk(kioskId,userId,userType,storeId,request));
    }

    @GetMapping()
    @Operation(summary = "키오스크 전체 조회 및 검색", description = "키오스크 이름으로 키오스크 계정을 조회합니다.")
    @ApiErrorCodeExamples({ErrorCode.INVALID_ROLE})
    public ResponseEntity<CommonResponse<CustomPage<KioskResponseDto>>> getKioskList(
            @RequestParam(required = false) String keyword,
            @PageableDefault(size=10, sort = "createdAt", direction = Sort.Direction.DESC)Pageable pageable,
            @AuthenticationPrincipal UserPrincipal userPrincipal){
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);

        return CommonResponse.ok(kioskService.getKioskList(storeId,userType,keyword,pageable));

    }
}
