package com.ssafy.mylio.domain.options.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class OptionListResponseDto {

    private List<OptionResponseDto> options;

    public static OptionListResponseDto of(List<OptionResponseDto> options) {
        return OptionListResponseDto.builder()
                .options(options)
                .build();
    }
}
