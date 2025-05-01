package com.ssafy.mylio.domain.category.dto.request;

import com.ssafy.mylio.domain.category.dto.response.CategoryResponseDto;
import com.ssafy.mylio.domain.category.entity.Category;
import com.ssafy.mylio.domain.store.entity.Store;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class CategoryAddRequestDto {

    @Schema(example = "음료")
    @NotNull(message = "nameKr 값은 필수입니다")
    @NotBlank(message = "카테고리를 입력해야합니다")
    private String nameKr;

    @Schema(example = "beverage")
    @NotNull(message = "nameEn 값은 필수입니다")
    @NotBlank(message = "카테고리를 입력해야합니다")
    private String nameEn;

    public Category toEntity(Store store) {
        return Category.builder()
                .store(store)
                .nameKr(this.nameKr)
                .nameEn(this.nameEn)
                .build();
    }
}
