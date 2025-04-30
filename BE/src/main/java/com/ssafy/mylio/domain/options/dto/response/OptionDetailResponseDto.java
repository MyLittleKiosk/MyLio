package com.ssafy.mylio.domain.options.dto.response;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class OptionDetailResponseDto {

    @Schema(example = "1")
    private Integer optionId;
    @Schema(example = "2")
    private Integer optionDetailId;
    @Schema(example = "아몬드 우유")
    private String optionDetailValue;
    @Schema(example = "500")
    private Integer additionalPrice;
    @Schema(example = "등록됨")
    private String status;
}
