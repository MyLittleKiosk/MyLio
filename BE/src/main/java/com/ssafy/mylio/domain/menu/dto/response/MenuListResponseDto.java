package com.ssafy.mylio.domain.menu.dto.response;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.menu.entity.MenuStatus;
import com.ssafy.mylio.domain.menu.entity.MenuTagMap;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class MenuListResponseDto {

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

    @Schema(example = "[\"인기\", \"여름\" ... ]")
    private List<String> tags;

    public static MenuListResponseDto of(Menu menu, List<String> tags){
        return MenuListResponseDto.builder()
                .menuId(menu.getId())
                .imageUrl(menu.getImageUrl())
                .nameKr(menu.getNameKr())
                .nameEn(menu.getNameEn())
                .category(menu.getCategory().getNameKr())
                .storeName(menu.getStore().getName())
                .description(menu.getDescription())
                .price(menu.getPrice())
                .status(menu.getStatus().getDescription())
                .tags(tags)
                .build();
    }

}
