package com.ssafy.mylio.domain.auth.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;

@Getter
public class KioskLoginRequest {
    @Schema(example = "1", description = "계정 ID (account.id)")
    @NotNull(message = "아이디는 필수 입력값입니다.")
    private Integer id;

    @Schema(example = "qwer1234",description ="비밀번호")
    @NotBlank(message = "비밀번호는 필수 입력값입니다.")
    private String password;

    @Schema(example = "1", description = "키오스크 ID (account.id)")
    @NotNull(message = "키오스크 아이디는 필수 입력값입니다.")
    private Integer kioskId;
}
