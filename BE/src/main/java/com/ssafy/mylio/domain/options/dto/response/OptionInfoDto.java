package com.ssafy.mylio.domain.options.dto.response;

import com.ssafy.mylio.domain.options.entity.MenuOptionMap;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class OptionInfoDto {
    @Schema(example = "1")
    private Integer menuOptionId;
    @Schema(example = "2")
    private Integer optionId;
    @Schema(example = "사이즈")
    private String optionNameKr;
    @Schema(example = "size")
    private String optionNameEn;
    @Schema(example = "S")
    private String optionValue;
    @Schema(example = "500")
    private Integer additionalPrice;
    @Schema(example = "true")
    private boolean isRequired;

    public static OptionInfoDto of (MenuOptionMap menuOptionMap){
        return  OptionInfoDto.builder()
                .menuOptionId(menuOptionMap.getId())
                .optionId(menuOptionMap.getOptions().getId())
                .optionNameKr(menuOptionMap.getOptions().getOptionNameKr())
                .optionNameEn(menuOptionMap.getOptions().getOptionNameEn())
                .optionValue(menuOptionMap.getOptionDetail().getValue())
                .additionalPrice(menuOptionMap.getOptionDetail().getAdditionalPrice())
                .isRequired(menuOptionMap.getIsRequired())
                .build();
    }

}
