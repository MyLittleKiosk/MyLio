package com.ssafy.mylio.domain.nutrition.dto.response;

import com.ssafy.mylio.domain.nutrition.entity.NutritionValue;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class NutritionInfoDto {
    @Schema(example = "1")
    private Integer menuNutritionId;
    @Schema(example = "2")
    private Integer nutritionId;
    @Schema(example = "단백질")
    private String nutritionNameKr;
    @Schema(example = "protein")
    private String nutritionNameEn;
    @Schema(example = "12g")
    private String nutritionValue;

    public static NutritionInfoDto of (NutritionValue nutritionValue) {
        return NutritionInfoDto.builder()
                .menuNutritionId(nutritionValue.getId())
                .nutritionId(nutritionValue.getNutrition().getId())
                .nutritionNameKr(nutritionValue.getNutrition().getNameKr())
                .nutritionNameEn(nutritionValue.getNutrition().getNameEn())
                .nutritionValue(nutritionValue.getValue().toString() + nutritionValue.getNutrition().getUnitType())
                .build();
    }
}
