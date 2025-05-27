package com.ssafy.mylio.domain.category.dto.response;

import com.ssafy.mylio.domain.category.entity.Category;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class CategoryResponseDto {

    @Schema(example = "1")
    private Integer categoryId;
    @Schema(example = "커피")
    private String nameKr;
    @Schema(example = "coffee")
    private String nameEn;

    public static CategoryResponseDto of(Category category){
        return CategoryResponseDto.builder()
                .categoryId(category.getId())
                .nameKr(category.getNameKr())
                .nameEn(category.getNameEn())
                .build();
    }
}
