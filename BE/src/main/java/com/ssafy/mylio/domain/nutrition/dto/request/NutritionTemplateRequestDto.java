package com.ssafy.mylio.domain.nutrition.dto.request;

import com.ssafy.mylio.domain.nutrition.entity.NutritionTemplate;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class NutritionTemplateRequestDto {
    @Schema(example = "단백질")
    private String nutritionTemplateName;
    @Schema(example = "protein")
    private String nutritionTemplateNameEn;
    @Schema(example = "g")
    private String nutritionTemplateType;

    public NutritionTemplate toEntity() {
        return NutritionTemplate.builder()
                .nameKr(this.nutritionTemplateName)
                .nameEn(this.nutritionTemplateNameEn)
                .unitType(this.nutritionTemplateType)
                .build();
    }
}
