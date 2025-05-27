package com.ssafy.mylio.domain.auth.dto.response;

import com.ssafy.mylio.domain.account.entity.Account;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@Schema(description = "SUPER 관리자 로그인 응답")
public class SuperInfoResponseDto implements LoginResponse{
    @Schema(example="1")
    private Integer userId;

    @Schema(example="홍길동")
    private String userName;

    @Schema(example="SUPER")
    private String role;

    public static SuperInfoResponseDto of(Account account){
        return SuperInfoResponseDto.builder()
                .userId(account.getId())
                .userName(account.getUsername())
                .role(account.getRole().getCode())
                .build();
    }

}
