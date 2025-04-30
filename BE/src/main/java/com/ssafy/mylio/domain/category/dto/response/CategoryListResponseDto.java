package com.ssafy.mylio.domain.category.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class CategoryListResponseDto {

    private List<CategoryResponseDto> categories;

    public static CategoryListResponseDto of (List<CategoryResponseDto> categories){
        return CategoryListResponseDto.builder()
                .categories(categories)
                .build();
    }
}
