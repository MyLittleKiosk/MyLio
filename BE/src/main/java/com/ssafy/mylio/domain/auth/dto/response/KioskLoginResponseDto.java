package com.ssafy.mylio.domain.auth.dto.response;

import com.ssafy.mylio.domain.account.entity.Account;
import com.ssafy.mylio.domain.account.entity.AccountRole;
import com.ssafy.mylio.domain.kiosk.entity.KioskSession;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@Schema(description = "키오스크 로그인 응답")
public class KioskLoginResponseDto implements LoginResponse{
    @Schema(example="1")
    private Integer storeId;

    @Schema(example="메가커피")
    private String storeName;

    @Schema(example="1")
    private Integer kioskId;

    @Schema(example="1")
    private Integer accountId;

    @Schema(example="KIOSK")
    private String role;

    @Schema(example="A")
    private String startOrder;

    public static KioskLoginResponseDto of(Account account, KioskSession kiosk, AccountRole role){
        return KioskLoginResponseDto.builder()
                .storeId(account.getStore().getId())
                .storeName(account.getStore().getName())
                .kioskId(kiosk.getId())
                .accountId(account.getId())
                .startOrder(kiosk.getStartOrderNumber())
                .role(role.getCode())
                .build();
    }

}
