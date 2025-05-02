package com.ssafy.mylio.domain.sales.dto.request;

import com.ssafy.mylio.domain.sales.entity.MonthlyCategorySalesRatio;
import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;
import java.util.List;

@Data
@Builder
public class CategorySalesResponseDto {
    private List<CategoryRatioDto> ratioByCategory;

    @Data
    @Builder
    public static class CategoryRatioDto {
        private String categoryName;
        private BigDecimal ratio;

        public static CategoryRatioDto of(String categoryName, BigDecimal ratio) {
            return CategoryRatioDto.builder()
                    .categoryName(categoryName)
                    .ratio(ratio)
                    .build();
        }
    }
}
