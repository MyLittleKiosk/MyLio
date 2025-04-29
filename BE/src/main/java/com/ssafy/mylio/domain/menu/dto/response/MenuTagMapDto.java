package com.ssafy.mylio.domain.menu.dto.response;

import com.ssafy.mylio.domain.menu.entity.MenuTagMap;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class MenuTagMapDto {

    @Schema(example = "1")
    private Integer tagId;
    @Schema(example = "달달해요")
    private String tagKr;
    @Schema(example = "sweet")
    private String tagEn;

    public static MenuTagMapDto of(MenuTagMap menuTagMap) {
        return MenuTagMapDto.builder()
                .tagId(menuTagMap.getId())
                .tagKr(menuTagMap.getTagKr())
                .tagEn(menuTagMap.getTagEn())
                .build();
    }
}
