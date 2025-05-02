package com.ssafy.mylio.domain.menu.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class MenuUpdateRequestDto {
    @Schema(example = "1")
    private Integer menuId;
    @Schema(example = "https://mylio")
    private String imageUrl;
    @Schema(example = "아이스 아메리카노")
    private String nameKr;
    @Schema(example = "ice americano")
    private String nameEn;
    @Schema(example = "커피")
    private String category;
    @Schema(example = "MaLio 강남점")
    private String storeName;
    @Schema(example = "MaLio 강남점")
    private String description;
    @Schema(example = "2000")
    private Integer price;
    @Schema(example = "판매")
    private String status;
}
