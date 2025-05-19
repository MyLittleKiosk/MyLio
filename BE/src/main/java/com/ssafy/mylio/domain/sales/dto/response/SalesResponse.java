package com.ssafy.mylio.domain.sales.dto.response;

import com.ssafy.mylio.domain.sales.entity.MonthlySalesSummary;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Builder;

@Getter
@Builder
public class SalesResponse {
    @Schema(example = "2",description = "연도별인 경우  1월,2월 .. 월별인 경우 1일, 2일 ..")
    private Integer element;

    @Schema(example = "200000",description = "총매출")
    private Integer sales;

    public SalesResponse of(MonthlySalesSummary data){
        return SalesResponse.builder()
                .element(data.getMonth())       // 1~12
                .sales(data.getTotalSales())
                .build();
    }
}