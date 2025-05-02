package com.ssafy.mylio.domain.kiosk.dto.response;

import com.ssafy.mylio.domain.kiosk.entity.KioskSession;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class KioskResponseDto {
    @Schema(example = "1")
    private Integer kioskId;

    @Schema(example = "A")
    private String startOrder;

    @Schema(example = "키오스크 01")
    private String name;

    @Schema(example = "false")
    private Boolean isActivate;

    public static KioskResponseDto of(KioskSession session){
        return KioskResponseDto.builder()
                .kioskId(session.getId())
                .startOrder(session.getStartOrderNumber())
                .name(session.getName())
                .isActivate(session.getIsActive())
                .build();
    }

}
