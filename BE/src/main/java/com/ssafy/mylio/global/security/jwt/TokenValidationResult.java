package com.ssafy.mylio.global.security.jwt;

public record TokenValidationResult(boolean isValid, TokenError error) {
}
