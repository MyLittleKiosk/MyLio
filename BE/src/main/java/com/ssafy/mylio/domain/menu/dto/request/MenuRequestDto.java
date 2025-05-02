package com.ssafy.mylio.domain.menu.dto.request;

import com.ssafy.mylio.domain.category.entity.Category;
import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.nutrition.dto.request.NutritionValuePostRequestDto;
import com.ssafy.mylio.domain.options.dto.request.MenuOptionMapRequestDto;
import com.ssafy.mylio.domain.store.entity.Store;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class MenuRequestDto {

    @Schema(example = "https://mylio/latte.jpg")
    private String imageUrl;
    @Schema(example = "아이스 아메리카노")
    private String nameKr;
    @Schema(example = "ice americano")
    private String nameEn;
    @Schema(example = "1")
    private Integer categoryId;
    @Schema(example = "어우 써!")
    private String description;
    @Schema(example = "2000")
    private Integer price;

    private List<TagRequestDto> tags;
    private List<NutritionValuePostRequestDto> nutritionInfo;
    private List<Integer> ingredientInfo;
    private List<MenuOptionMapRequestDto> optionInfo;

    public Menu toEntity(Store store, Category category){
        return Menu.builder()
                .store(store)
                .category(category)
                .imageUrl(this.imageUrl)
                .nameKr(this.nameKr)
                .nameEn(this.nameEn)
                .description(this.description)
                .price(this.price)
                .build();
    }
}
