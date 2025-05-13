package com.ssafy.mylio.domain.nutrition.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class NutritionTemplateUpdateRequestDto {
    @Schema(example = "1")
    private Integer nutritionTemplateId;
    @Schema(example = "단백질")
    private String nutritionTemplateName;
    @Schema(example = "protein")
    private String nutritionTemplateNameEn;
    @Schema(example = "g")
    private String nutritionTemplateType;
}
