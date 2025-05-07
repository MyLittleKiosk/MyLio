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
    private Integer accountId;

    @Schema(example="qwer@ssafy.io")
    private String email;

    @Schema(example="마리오")
    private String userName;

    @Schema(example="싸피 다방")
    private String storeName;

    @Schema(example="경기도 다낭")
    private String address;

    public static AccountModifyResponse of(Account account){
        return AccountModifyResponse.builder()
                .accountId(account.getId())
                .email(account.getEmail())
                .userName(account.getUsername())
                .storeName(account.getStore().getName())
                .address(account.getStore().getAddress())
                .build();
    }

}
