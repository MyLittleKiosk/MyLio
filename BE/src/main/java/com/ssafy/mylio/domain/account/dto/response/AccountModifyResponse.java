package com.ssafy.mylio.domain.account.dto.response;

import com.ssafy.mylio.domain.account.entity.Account;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@Schema(description = "계정 수정 response")
public class AccountModifyResponse {
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


    public static AccountModifyResponse of(Account account){
        return AccountModifyResponse.builder()
                .userId(account.getId())
                .storeId(account.getStore().getId())
                .userName(account.getUsername())
                .role(account.getRole().getCode())
                .status(account.getStatus().getCode())
                .build();
    }

}
