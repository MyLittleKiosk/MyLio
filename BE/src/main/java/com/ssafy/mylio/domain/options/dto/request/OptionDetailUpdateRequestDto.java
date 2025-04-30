package com.ssafy.mylio.domain.options.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.PositiveOrZero;
import lombok.Builder;
import lombok.Getter;

import javax.validation.constraints.NotNull;

@Getter
@Builder
public class OptionDetailUpdateRequestDto {

    @Schema(example = "아몬드 우유")
    private String value;

    @Schema(example = "500")
    @PositiveOrZero(message = "추가가격은 0이상의 숫자를 입력해야합니다")
    private Integer additionalPrice;

    @Schema(example = "HIDDEN")
    private String status;
}
