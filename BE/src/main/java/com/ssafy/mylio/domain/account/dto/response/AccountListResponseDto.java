package com.ssafy.mylio.domain.account.dto.response;

import com.ssafy.mylio.domain.account.entity.Account;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class AccountListResponseDto {
    @Schema(example = "i")
    private Integer accountId;

    @Schema(example = "마리오")
    private String userName;

    @Schema(example = "test1@ssafy.io")
    private String email;

    @Schema(example = "싸피다방")
    private String storeName;

    public static AccountListResponseDto of(Account account){
        return AccountListResponseDto.builder()
                .accountId(account.getId())
                .userName(account.getUsername())
                .email(account.getEmail())
                .storeName(account.getStore().getName())
                .build();
    }
}
