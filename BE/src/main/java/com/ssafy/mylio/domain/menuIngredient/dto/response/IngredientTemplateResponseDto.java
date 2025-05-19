package com.ssafy.mylio.domain.menuIngredient.dto.response;

import com.ssafy.mylio.domain.menuIngredient.entity.IngredientTemplate;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class IngredientTemplateResponseDto {
    @Schema(example = "1")
    private Integer ingredientTemplateId;
    @Schema(example = "우유")
    private String ingredientTemplateName;
    @Schema(example = "milk")
    private String ingredientTemplateNameEn;

    public static IngredientTemplateResponseDto of(IngredientTemplate ingredientTemplate){
        return IngredientTemplateResponseDto.builder()
                .ingredientTemplateId(ingredientTemplate.getId())
                .ingredientTemplateName(ingredientTemplate.getNameKr())
                .ingredientTemplateNameEn(ingredientTemplate.getNameEn())
                .build();
    }
}
