package com.ssafy.mylio.domain.account.dto.response;

import com.ssafy.mylio.domain.account.entity.Account;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@Schema(description = "계정 생성 response")
public class AccountCreateResponseDto {
    @Schema(example="1")
    private Integer userId;

    @Schema(example="1")
    private Integer storeId;

    @Schema(example="마리오")
    private String userName;

    @Schema(example="STORE")
    private String role;

    @Schema(example="REGISTERED")
    private String status;

    @Schema(example="qwer1234")
    private String password;

    public static AccountCreateResponseDto of(Account account){
        return AccountCreateResponseDto.builder()
                .userId(account.getId())
                .storeId(account.getStore().getId())
                .userName(account.getUsername())
                .role(account.getRole().getCode())
                .password(account.getPassword())
                .status(account.getStatus().getCode())
                .build();
    }

}
