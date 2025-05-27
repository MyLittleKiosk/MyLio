package com.ssafy.mylio.domain.account.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Getter;

@Getter
public class ModifyPasswordRequest {
    @Schema(example = "qwer1234",description = "현재 비밀번호입니다.")
    @NotBlank(message = "현재 비밀번호는 필수입니다.")
    private String nowPw;


    @Schema(example = "1234qwer",description = "변경할 비밀번호입니다.")
    @NotBlank(message = "변경할 비밀번호는 필수입니다.")
    private String newPw;
}
