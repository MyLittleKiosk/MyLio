package com.ssafy.mylio.domain.auth.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import jakarta.validation.constraints.NotBlank;

@Getter
public class AdminLoginRequestDto {
    @Schema(example = "qwer@ssafy.io", description = "이메일")
    @NotNull(message = "이메일은 필수 입력값입니다.")
    private String email;

    @Schema(example = "qwer1234",description ="비밀번호")
    @NotBlank(message = "비밀번호는 필수 입력값입니다.")
    private String password;
}
