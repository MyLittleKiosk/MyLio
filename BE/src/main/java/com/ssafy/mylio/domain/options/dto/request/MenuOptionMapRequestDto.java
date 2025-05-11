package com.ssafy.mylio.domain.options.dto.request;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.options.entity.MenuOptionMap;
import com.ssafy.mylio.domain.options.entity.OptionDetail;
import com.ssafy.mylio.domain.options.entity.Options;
import com.ssafy.mylio.domain.store.entity.Store;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class MenuOptionMapRequestDto {
    @Schema(example = "1")
    private Integer optionId;
    @Schema(example = "true")
    private boolean isRequired;
    @Schema(example = "1")
    private Integer optionDetailId;

    public MenuOptionMap toEntity(Menu menu, Options options, OptionDetail optionDetail){
        return MenuOptionMap.builder()
                .menu(menu)
                .options(options)
                .optionDetail(optionDetail)
                .isRequired(this.isRequired)
                .build();
    }
}