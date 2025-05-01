package com.ssafy.mylio.domain.account.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Getter;

@Getter
public class PasswordRequestDto {
    @Schema(example = "test1@ssafy")
    @NotBlank(message = "이메일은 필수 입력값입니다.")
    private String email;

    @Schema(example = "홍길동")
    @NotBlank(message = "사용자이름은 필수 입력값입니다.")
    private String username;
}
