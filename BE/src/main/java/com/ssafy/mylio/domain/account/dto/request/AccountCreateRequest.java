package com.ssafy.mylio.domain.account.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;

@Getter
public class AccountCreateRequest {
    @Schema(example = "qwer@ssafy.io", description = "이메일")
    @NotNull(message = "이메일은 필수 입력값입니다.")
    private String email;

    @Schema(example = "마리오")
    @NotBlank(message = "user_name은 필수입니다.")
    private String userName;

    @Schema(example="싸피다방")
    @NotBlank(message = "매장 이름을 필수입니다.")
    private String storeName;

    @Schema(example="경기도 다낭시")
    @NotBlank(message = "주소는 필수입니다.")
    private String address;

}
