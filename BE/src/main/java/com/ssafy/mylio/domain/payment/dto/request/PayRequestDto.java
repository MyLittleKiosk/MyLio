package com.ssafy.mylio.domain.payment.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class PayRequestDto {
    @Schema(example = "A101")
    private String sessionId;
    @Schema(example = "아이스 아메리카노")
    private String itemName;
    @Schema(example = "1500")
    private int totalAmount;
}
