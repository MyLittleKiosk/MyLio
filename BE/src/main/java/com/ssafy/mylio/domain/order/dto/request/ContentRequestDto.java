package com.ssafy.mylio.domain.order.dto.request;

import com.ssafy.mylio.domain.order.dto.common.NutritionInfoDto;
import com.ssafy.mylio.domain.order.dto.common.OptionsDto;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class ContentRequestDto {
    @Schema(example = "1")
    private Integer menuId;
    @Schema(example = "1")
    private Integer quantity;
    @Schema(example = "바닐라 라떼")
    private String name;
    @Schema(example = "바닐라 시럽이 달콤하게 어우러진 라떼")
    private String description;
    @Schema(example = "3000")
    private Integer basePrice;
    @Schema(example = "3500")
    private Integer totalPrice;
    @Schema(example = "vanillalatte.jpg")
    private String imageUrl;
    @Schema(example = "CARD")
    private List<OptionsDto> options;
    private List<OptionsDto> selectedOption;
    private List<NutritionInfoDto> nutritionInfo;
}
