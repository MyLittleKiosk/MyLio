package com.ssafy.mylio.domain.auth.controller;


import com.ssafy.mylio.domain.auth.dto.LoginResult;
import com.ssafy.mylio.domain.auth.dto.request.AdminLoginRequestDto;
import com.ssafy.mylio.domain.auth.dto.request.KioskLoginRequest;
import com.ssafy.mylio.domain.auth.dto.request.LogoutRequest;
import com.ssafy.mylio.domain.auth.dto.response.LoginResponse;
import com.ssafy.mylio.domain.auth.service.AuthService;
import com.ssafy.mylio.global.aop.swagger.ApiErrorCodeExamples;
import com.ssafy.mylio.global.common.response.CommonResponse;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import com.ssafy.mylio.global.util.AuthenticationUtil;
import com.ssafy.mylio.global.util.CookieUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseCookie;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;
import com.ssafy.mylio.global.error.code.ErrorCode;

@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
@Tag(name = "인증", description="인증 & 인가 API")
public class AuthController {
    private final AuthService authService;
    private final AuthenticationUtil authenticationUtil;

    @PostMapping("/login")
    @Operation(summary = "슈퍼 / 관리자 로그인", description = "슈퍼 관리자, 관리자의 로그인 API 입니다.\n\n관리자 역할에 따라 다른 dto를 반환합니다.")
    @ApiErrorCodeExamples({ErrorCode.INTERNAL_SERVER_ERROR, ErrorCode.INVALID_CREDENTIALS})
    public ResponseEntity<CommonResponse<LoginResponse>> adminLogin(
            @Valid @RequestBody AdminLoginRequestDto request){
        LoginResult result = authService.login(request);


        ResponseCookie accessTokenCookie = CookieUtil.makeAccessTokenCookie(result.getAccessToken());
        ResponseCookie refreshTokenCookie = CookieUtil.makeRefreshTokenCookie(result.getRefreshToken());

        return CommonResponse.okWithCookie(
                result.getResponse(),
                accessTokenCookie,
                refreshTokenCookie
        );
    }

    @PostMapping("/refresh")
    @Operation(summary = "토큰 갱신", description = "리프레시 토큰을 사용하여 액세스 토큰을 갱신합니다.")
    @ApiErrorCodeExamples({ErrorCode.INTERNAL_SERVER_ERROR, ErrorCode.INVALID_REFRESH_TOKEN})
    public ResponseEntity<CommonResponse<Void>> refreshToken(
            @CookieValue(name = "refresh_token",required = false) String refreshToken){
        ResponseCookie accessTokenCookie = CookieUtil.makeAccessTokenCookie(authService.getRefreshToken(refreshToken));

        return CommonResponse.okWithCookie(accessTokenCookie);

    }

    @PostMapping("/login/kiosk")
    @Operation(summary = "키오스크 로그인", description = "키오스크 로그인 API 입니다.\n\n키오스크 ID에 따라 startOrder를 다르게 반환합니다.")
    @ApiErrorCodeExamples({ErrorCode.INTERNAL_SERVER_ERROR, ErrorCode.INVALID_CREDENTIALS,ErrorCode.INVALID_ROLE,ErrorCode.STORE_NOT_FOUND,ErrorCode.KIOSK_SESSION_NOT_FOUND,ErrorCode.KIOSK_IN_USE})
    public ResponseEntity<CommonResponse<LoginResponse>> kioskLogin(
            @Valid @RequestBody KioskLoginRequest request){
        LoginResult result = authService.kioskLogin(request);

        ResponseCookie accessTokenCookie = CookieUtil.makeAccessTokenCookie(result.getAccessToken());
        ResponseCookie refreshTokenCookie = CookieUtil.makeRefreshTokenCookie(result.getRefreshToken());

        return CommonResponse.okWithCookie(
                result.getResponse(),
                accessTokenCookie,
                refreshTokenCookie
        );
    }

    @PostMapping("/logout")
    @Operation(summary = "공통 로그아웃",description="로그인된 사용자를 로그아웃 처리합니다.\n\n키오스크 로그인의 경우 body에 kiosk_id가 필수 입니다.")
    public ResponseEntity<CommonResponse<Void>> logout(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestBody(required = false)LogoutRequest request
            ){
        Integer userId = authenticationUtil.getCurrentUserId(userPrincipal);
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);

        authService.logout(userId,userType,request);

        // 쿠키 삭제
        ResponseCookie deleteAccessToken = CookieUtil.deleteAccessTokenCookie();
        ResponseCookie deleteRefreshToken = CookieUtil.deleteRefreshTokenCookie();

        return CommonResponse.okWithCookie(deleteAccessToken, deleteRefreshToken);
    }
}
