package com.ssafy.mylio.domain.nutrition.dto.response;

import com.ssafy.mylio.domain.nutrition.entity.NutritionValue;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import java.math.BigDecimal;

@Getter
@Builder
public class NutritionResponseDto {
    @Schema(example = "1")
    private Integer  nutritionId;
    @Schema(example = "10")
    private BigDecimal nutritionValue;
    @Schema(example = "1")
    private Integer nutritionTemplateId;
    @Schema(example = "단백질")
    private String nutritionTemplateName;
    @Schema(example = "g")
    private String nutritionTemplateType;

    public static NutritionResponseDto of(NutritionValue nutritionValue){
        return NutritionResponseDto.builder()
                .nutritionId(nutritionValue.getId())
                .nutritionValue(nutritionValue.getValue())
                .nutritionTemplateId(nutritionValue.getNutrition().getId())
                .nutritionTemplateName(nutritionValue.getNutrition().getNameKr())
                .nutritionTemplateType(nutritionValue.getNutrition().getUnitType())
                .build();
    }
}
