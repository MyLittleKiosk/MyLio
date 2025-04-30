package com.ssafy.mylio.domain.account.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;

@Getter
public class AccountCreateRequest {
    @Schema(example = "1", description = "매장 ID (store.id)")
    @NotNull(message = "storeId는 필수 입력값입니다.")
    private Integer storeId;

    @Schema(example = "마리오")
    @NotBlank(message = "user_name은 필수입니다.")
    private String userName;

    @Schema(example="qwer1234")
    @NotBlank(message = "비밀번호는 필수 입니다.")
    @Size(min = 8, max = 16)
    private String password;

}
