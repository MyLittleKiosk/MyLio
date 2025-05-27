package com.ssafy.mylio.domain.sales.dto.response;

import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;
import java.util.List;

@Data
@Builder
public class CategorySalesResponseDto {

    private String categoryName;
    private BigDecimal ratio;

    public static CategorySalesResponseDto of(String categoryName, BigDecimal ratio) {
        return CategorySalesResponseDto.builder()
                .categoryName(categoryName)
                .ratio(ratio)
                .build();
    }

}
