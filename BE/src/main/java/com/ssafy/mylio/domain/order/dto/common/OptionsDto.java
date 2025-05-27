package com.ssafy.mylio.domain.order.dto.common;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder(toBuilder = true)
public class OptionsDto {
    @Schema(example = "1")
    private Integer optionId;
    @Schema(example = "온도")
    private String optionName;
    @Schema(example = "true")
    private boolean required;
    @JsonProperty("isSelected")
    @Schema(example = "true")
    private boolean isSelected;
    @Schema(example = "1")
    private Integer selectedId;
    private List<OptionDetailsDto> optionDetails;
}
