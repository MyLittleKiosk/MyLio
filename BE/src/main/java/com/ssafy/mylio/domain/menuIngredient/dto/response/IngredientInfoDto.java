package com.ssafy.mylio.domain.menuIngredient.dto.response;

import com.ssafy.mylio.domain.menuIngredient.entity.MenuIngredient;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class IngredientInfoDto {
    @Schema(example = "1")
    private Integer menuIngredientId;
    @Schema(example = "2")
    private Integer ingredientId;
    @Schema(example = "우유")
    private String ingredientNameKr;
    @Schema(example = "milk")
    private String ingredientNameEn;

    public static IngredientInfoDto of (MenuIngredient menuIngredient) {
        return IngredientInfoDto.builder()
                .menuIngredientId(menuIngredient.getId())
                .ingredientId(menuIngredient.getIngredient().getId())
                .ingredientNameKr(menuIngredient.getIngredient().getNameKr())
                .ingredientNameEn(menuIngredient.getIngredient().getNameEn())
                .build();
    }
}
