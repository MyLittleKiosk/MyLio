package com.ssafy.mylio.domain.options.dto.response;

import com.ssafy.mylio.domain.options.entity.Options;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class OptionResponseDto {

    @Schema(example = "2")
    private Integer optionId;
    @Schema(example = "사이즈")
    private String optionNameKr;
    @Schema(example = "size")
    private String optionNameEn;

    private List<OptionDetailDto> optionDetails;

    public static OptionResponseDto of (Options options, List<OptionDetailDto> optionDetails){
        return OptionResponseDto.builder()
                .optionId(options.getId())
                .optionNameKr(options.getOptionNameKr())
                .optionNameEn(options.getOptionNameEn())
                .optionDetails(optionDetails)
                .build();
    }
}