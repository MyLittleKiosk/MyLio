package com.ssafy.mylio.domain.nutrition.dto.response;

import com.ssafy.mylio.domain.nutrition.entity.NutritionTemplate;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class NutritionTemplateResponseDto {
    @Schema(example = "1")
    private Integer nutritionTemplateId;
    @Schema(example = "단백질")
    private String nutritionTemplateName;
    @Schema(example = "protein")
    private String nutritionTemplateNameEn;
    @Schema(example = "g")
    private String nutritionTemplateType;

    public static NutritionTemplateResponseDto of(NutritionTemplate nutritionTemplate){
        return NutritionTemplateResponseDto.builder()
                .nutritionTemplateId(nutritionTemplate.getId())
                .nutritionTemplateName(nutritionTemplate.getNameKr())
                .nutritionTemplateNameEn(nutritionTemplate.getNameEn())
                .nutritionTemplateType(nutritionTemplate.getUnitType())
                .build();
    }
}
