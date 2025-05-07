package com.ssafy.mylio.domain.order.dto.response;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class OptionsResponseDto {
    @Schema(example = "1")
    private Integer optionId;
    @Schema(example = "온도")
    private String optionName;
    @Schema(example = "true")
    private boolean required;
    @Schema(example = "true")
    private boolean isSelected;
    private List<OptionDetailsResponseDto> optionDetails;
}
