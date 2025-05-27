package com.ssafy.mylio.domain.sales.dto.response;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class DailySalesResponseDto {
    @Schema(example = "1000000",description = "총 매출")
    private Integer totalSales;

    @Schema(example = "30",description = "총 주문 건수")
    private Integer totalOrders;

    public static DailySalesResponseDto of(Integer sales, Integer orders){
        return DailySalesResponseDto.builder()
                .totalSales(sales)
                .totalOrders(orders)
                .build();
    }
}
