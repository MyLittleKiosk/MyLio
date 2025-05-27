package com.ssafy.mylio.domain.category.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class CategoryUpdateRequestDto {

    @Schema(example = "음료")
    @NotBlank(message = "nameKr 값은 필수입니다")
    private String nameKr;

    @Schema(example = "beverage")
    @NotBlank(message = "nameEn 값은 필수입니다")
    private String nameEn;

    @Schema(example = "REGISTERED")
    @NotBlank(message = "status 값은 필수입니다")
    private String status;
}
