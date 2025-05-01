package com.ssafy.mylio.domain.options.dto.response;

import com.ssafy.mylio.domain.options.entity.OptionDetail;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class OptionDetailDto {
    @Schema(example = "2")
    private Integer optionDetailId;
    @Schema(example = "S")
    private String optionDetailValue;
    @Schema(example = "500")
    private Integer additionalPrice;

    public static OptionDetailDto of(OptionDetail optionDetail) {
        return OptionDetailDto.builder()
                .optionDetailId(optionDetail.getId())
                .optionDetailValue(optionDetail.getValue())
                .additionalPrice(optionDetail.getAdditionalPrice())
                .build();
    }
}
