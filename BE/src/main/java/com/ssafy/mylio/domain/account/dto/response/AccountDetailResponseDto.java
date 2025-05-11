package com.ssafy.mylio.domain.account.dto.response;

import com.ssafy.mylio.domain.account.entity.Account;
import com.ssafy.mylio.domain.store.entity.Store;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class AccountDetailResponseDto {
    @Schema(example = "1", description = "매장 관리자 아이디입니다.")
    private Integer accountId;

    @Schema(example = "홍길동", description = "매장 관리자 이름입니다.")
    private String userName;

    @Schema(example = "test1@ssafy.io", description = "매장 관리자 이메일입니다.")
    private String email;

    @Schema(example = "싸피다방", description = "매장 이름입니다.")
    private String storeName;

    @Schema(example = "경기도 다낭시", description = "매장 주소입니다.")
    private String address;

    public static AccountDetailResponseDto of(Account account, Store store){
        return AccountDetailResponseDto.builder()
                .accountId(account.getId())
                .userName(account.getUsername())
                .email(account.getEmail())
                .storeName(store.getName())
                .address(store.getAddress())
                .build();
    }

}
