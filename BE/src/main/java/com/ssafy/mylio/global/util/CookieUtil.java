package com.ssafy.mylio.global.util;


import com.ssafy.mylio.global.common.constants.SecurityConstants;
import org.springframework.http.ResponseCookie;

import java.time.Duration;

public class CookieUtil {
    public static ResponseCookie makeAccessTokenCookie(String refreshToken) {
        return ResponseCookie.from(SecurityConstants.ACCESS_TOKEN_COOKIE_NAME, refreshToken)
                .httpOnly(true)
                .secure(!SecurityConstants.getIsLocal()) // isLocal이 true면 secure=false, false면 secure=true
                .sameSite(SecurityConstants.getIsLocal() ? "Lax" : "None") // isLocal이 true면 Lax, false면 None
                .domain(SecurityConstants.getDomain())
                .path("/") // 모든 경로에서 접근 가능
                .maxAge(Duration.ofSeconds(SecurityConstants.ACCESS_TOKEN_VALIDITY_SECONDS))
                .build();
    }

    public static ResponseCookie makeRefreshTokenCookie(String refreshToken) {
        return ResponseCookie.from(SecurityConstants.REFRESH_TOKEN_COOKIE_NAME, refreshToken)
                .httpOnly(true)
                .secure(!SecurityConstants.getIsLocal())
                .sameSite(SecurityConstants.getIsLocal() ? "Lax" : "None")
                .domain(SecurityConstants.getDomain())
                .path("/") // 모든 경로에서 접근 가능
                .maxAge(Duration.ofSeconds(SecurityConstants.REFRESH_TOKEN_VALIDITY_SECONDS))
                .build();
    }

    public static ResponseCookie deleteAccessTokenCookie() {
        return ResponseCookie.from(SecurityConstants.ACCESS_TOKEN_COOKIE_NAME, "")
                .httpOnly(true)
                .secure(!SecurityConstants.getIsLocal())
                .sameSite(SecurityConstants.getIsLocal() ? "Lax" : "None")
                .domain(SecurityConstants.getDomain())
                .path("/")
                .maxAge(0) // 즉시 만료
                .build();
    }

    public static ResponseCookie deleteRefreshTokenCookie() {
        return ResponseCookie.from(SecurityConstants.REFRESH_TOKEN_COOKIE_NAME, "")
                .httpOnly(true)
                .secure(!SecurityConstants.getIsLocal())
                .sameSite(SecurityConstants.getIsLocal() ? "Lax" : "None")
                .domain(SecurityConstants.getDomain())
                .path("/")
                .maxAge(0) // 즉시 만료
                .build();
    }

    public static ResponseCookie makeDevAccessTokenCookie(String refreshToken) {
        return ResponseCookie.from(SecurityConstants.ACCESS_TOKEN_COOKIE_NAME, refreshToken)
                .httpOnly(false)
                .secure(true)
                .sameSite("None")
                .domain(null)
                .path("/")
                .maxAge(Duration.ofSeconds(SecurityConstants.ACCESS_TOKEN_VALIDITY_SECONDS))
                .build();
    }

    public static ResponseCookie makeDevRefreshTokenCookie(String refreshToken) {
        return ResponseCookie.from(SecurityConstants.REFRESH_TOKEN_COOKIE_NAME, refreshToken)
                .httpOnly(false)
                .secure(true)
                .sameSite("None")
                .domain(null)
                .path("/")
                .maxAge(Duration.ofSeconds(SecurityConstants.REFRESH_TOKEN_VALIDITY_SECONDS))
                .build();
    }
}
