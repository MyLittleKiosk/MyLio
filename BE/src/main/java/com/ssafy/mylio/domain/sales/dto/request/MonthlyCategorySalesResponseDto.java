package com.ssafy.mylio.domain.sales.dto.request;

import com.ssafy.mylio.domain.sales.entity.MonthlyCategorySalesRatio;
import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;
import java.util.List;

@Data
@Builder
public class MonthlyCategorySalesResponseDto {
    private List<CategoryRatioDto> ratioByCategory;

    @Data
    @Builder
    public static class CategoryRatioDto {
        private String categoryName;
        private BigDecimal ratio;

        public static CategoryRatioDto of(MonthlyCategorySalesRatio monthlyCategorySalesRatio){
            return CategoryRatioDto.builder()
                    .categoryName(monthlyCategorySalesRatio.getCategory().getNameKr())
                    .ratio(monthlyCategorySalesRatio.getRatio())
                    .build();
        }
    }
}
