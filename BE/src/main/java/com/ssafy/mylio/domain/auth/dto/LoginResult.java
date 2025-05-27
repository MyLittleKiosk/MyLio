package com.ssafy.mylio.domain.auth.dto;

import com.ssafy.mylio.domain.auth.dto.response.LoginResponse;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class LoginResult {
    private LoginResponse response;
    private String accessToken;
    private String refreshToken;

    public static LoginResult of(LoginResponse response, String accessToken, String refreshToken) {
        return LoginResult.builder()
                .response(response)
                .accessToken(accessToken)
                .refreshToken(refreshToken)
                .build();
    }
}
