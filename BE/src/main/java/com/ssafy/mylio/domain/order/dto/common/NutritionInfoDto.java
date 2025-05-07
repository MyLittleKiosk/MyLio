package com.ssafy.mylio.domain.order.dto.common;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class NutritionInfoDto {
    @Schema(example = "1")
    private Integer nutritionId;
    @Schema(example = "단백질")
    private String nutritionName;
    @Schema(example = "12")
    private Integer nutritionValue;
    @Schema(example = "g")
    private String nutritionType;
}
