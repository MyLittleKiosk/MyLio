package com.ssafy.mylio.domain.sales.dto.response;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import java.math.BigDecimal;

@Getter
@Builder
public class OrderTypeSalesResponseDto {
    @Schema(example = "매장",description = "매장 / 포장")
    private String orderTypeName;

    @Schema(example = "40.6", description = "비율")
    private BigDecimal ratio;

    public static OrderTypeSalesResponseDto of(String orderTypeName, BigDecimal ratio){
        return OrderTypeSalesResponseDto.builder()
                .orderTypeName(orderTypeName)
                .ratio(ratio)
                .build();
    }
}
