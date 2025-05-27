package com.ssafy.mylio.domain.auth.dto.response;

import com.ssafy.mylio.domain.account.entity.Account;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@Schema(description = "관리자 로그인 응답")
public class StoreInfoResponseDto implements LoginResponse{
    @Schema(example="1")
    private Integer userId;

    @Schema(example="1")
    private Integer storeId;

    @Schema(example="메가커피")
    private String storeName;

    @Schema(example="STORE")
    private String role;

    public static StoreInfoResponseDto of(Account account){
        return StoreInfoResponseDto.builder()
                .userId(account.getId())
                .storeId(account.getStore().getId())
                .storeName(account.getStore().getName())
                .role(account.getRole().getCode())
                .build();
    }

}
