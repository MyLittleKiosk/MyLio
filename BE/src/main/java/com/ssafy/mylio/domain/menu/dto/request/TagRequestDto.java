package com.ssafy.mylio.domain.menu.dto.request;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.menu.entity.MenuTagMap;
import com.ssafy.mylio.domain.store.entity.Store;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class TagRequestDto {
    @Schema(example = "달달")
    private String tagKr;
    @Schema(example = "sweet")
    private String tagEn;

    public MenuTagMap toEntity(Menu menu, Store store){
        return MenuTagMap.builder()
                .menu(menu)
                .store(store)
                .tagKr(this.tagKr)
                .tagEn(this.tagEn)
                .build();
    }
}
