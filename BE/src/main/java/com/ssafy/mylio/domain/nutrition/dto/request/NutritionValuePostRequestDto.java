package com.ssafy.mylio.domain.nutrition.dto.request;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.nutrition.entity.NutritionTemplate;
import com.ssafy.mylio.domain.nutrition.entity.NutritionValue;
import com.ssafy.mylio.domain.store.entity.Store;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import java.math.BigDecimal;

@Getter
@Builder
public class NutritionValuePostRequestDto {

    @Schema(example = "1")
    private Integer nutritionTemplateId;
    @Schema(example = "12")
    private BigDecimal nutritionValue;

    public NutritionValue toEntity(Store store, Menu menu, NutritionTemplate nutritionTemplate){
        return NutritionValue.builder()
                .store(store)
                .menu(menu)
                .nutrition(nutritionTemplate)
                .value(this.nutritionValue)
                .build();
    }
}