package com.ssafy.mylio.domain.menu.dto.response;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.menuIngredient.dto.response.IngredientInfoDto;
import com.ssafy.mylio.domain.nutrition.dto.response.NutritionInfoDto;
import com.ssafy.mylio.domain.options.dto.response.OptionInfoDto;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class MenuDetailResponseDto {

    private MenuInfoDto menuInfo;
    private List<MenuTagMapDto> tags;
    private List<NutritionInfoDto> nutritionInfo;
    private List<IngredientInfoDto> ingredientInfo;
    private List<OptionInfoDto> optionInfo;

    public static MenuDetailResponseDto of (Menu menu,
                                            List<MenuTagMapDto> tags,
                                            List<NutritionInfoDto> nutritionInfo,
                                            List<IngredientInfoDto> ingredientInfo,
                                            List<OptionInfoDto> optionInfo) {

        return MenuDetailResponseDto.builder()
                .menuInfo(MenuInfoDto.of(menu))
                .tags(tags)
                .nutritionInfo(nutritionInfo)
                .ingredientInfo(ingredientInfo)
                .optionInfo(optionInfo)
                .build();
    }

}
