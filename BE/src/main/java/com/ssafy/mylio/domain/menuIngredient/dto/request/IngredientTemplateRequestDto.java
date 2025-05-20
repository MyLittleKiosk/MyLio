package com.ssafy.mylio.domain.menuIngredient.dto.request;

import com.ssafy.mylio.domain.menuIngredient.entity.IngredientTemplate;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class IngredientTemplateRequestDto {

    @Schema(example = "우유")
    private String ingredientTemplateName;
    @Schema(example = "milk")
    private String ingredientTemplateNameEn;

    public IngredientTemplate toEntity(){
        return IngredientTemplate.builder()
                .nameKr(this.ingredientTemplateName)
                .nameEn(this.ingredientTemplateNameEn)
                .build();
    }
}
