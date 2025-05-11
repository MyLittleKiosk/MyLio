package com.ssafy.mylio.domain.account.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;

@Getter
public class AccountModifyRequestDto {

    @Schema(example = "마리오")
    @NotBlank(message = "user_name은 필수입니다.")
    private String userName;

    @Schema(example="qwer@ssafy.io")
    @NotBlank(message = "이메일은 필수 입니다.")
    private String email;

    @Schema(example = "싸피 다방")
    @NotBlank(message = "매장 이름은 필수입니다.")
    private String storeName;

    @Schema(example = "경기도 다낭")
    @NotBlank(message = "매장 주소는 필수입니다.")
    private String address;

}
