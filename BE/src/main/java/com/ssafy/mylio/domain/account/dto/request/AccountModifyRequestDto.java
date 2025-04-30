package com.ssafy.mylio.domain.account.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;

@Getter
public class AccountModifyRequestDto {
    @Schema(example="1", description = "매장 관리자 ID (account.id)")
    @NotNull(message = "storeId는 필수 입력값입니다.")
    private Integer userId;

    @Schema(example = "1", description = "매장 ID (store.id)")
    @NotNull(message = "storeId는 필수 입력값입니다.")
    private Integer storeId;

    @Schema(example = "마리오")
    @NotBlank(message = "user_name은 필수입니다.")
    private String userName;

    @Schema(example="qwer1234")
    @NotBlank(message = "비밀번호는 필수 입니다.")
    private String password;

    @Schema(example="REGISTERED")
    @NotBlank(message = "상태값은 필수입니다.")
    private String status;

}
