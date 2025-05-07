package com.ssafy.mylio.domain.order.dto.common;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class OptionDetailsDto {
    @Schema(example = "1")
    private Integer optionDetailId;
    @Schema(example = "ICE")
    private String optionDetailValue;
    @Schema(example = "500")
    private Integer additionalPrice;
}
