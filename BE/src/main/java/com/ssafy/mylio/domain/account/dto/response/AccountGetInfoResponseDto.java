package com.ssafy.mylio.domain.account.dto.response;

import com.ssafy.mylio.domain.account.entity.Account;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class AccountGetInfoResponseDto {
    @Schema(example = "SUPER", description = "로그인한 계정의 역할입니다.")
    private String role;

    @Schema(example = "1", description = "로그인한 계정의 아이디입니다.")
    private Integer userID;

    public static AccountGetInfoResponseDto of(Account account,String userRole){
        return AccountGetInfoResponseDto.builder()
                .role(userRole)
                .userID(account.getId())
                .build();
    }

}
