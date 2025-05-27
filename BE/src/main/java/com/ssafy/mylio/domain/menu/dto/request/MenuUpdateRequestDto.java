package com.ssafy.mylio.domain.menu.dto.request;

import com.ssafy.mylio.domain.category.entity.Category;
import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.nutrition.dto.request.NutritionValuePostRequestDto;
import com.ssafy.mylio.domain.options.dto.request.MenuOptionMapRequestDto;
import com.ssafy.mylio.domain.store.entity.Store;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;

import java.util.List;

@Getter
@SuperBuilder
@NoArgsConstructor
public class MenuUpdateRequestDto extends MenuRequestDto {

    @Schema(example = "https://mylio/latte.jpg")
    private String imageUrl;

}
