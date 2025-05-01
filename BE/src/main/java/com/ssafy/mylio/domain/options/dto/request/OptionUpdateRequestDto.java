package com.ssafy.mylio.domain.options.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Builder;
import lombok.Getter;

import javax.validation.constraints.NotNull;

@Getter
@Builder
public class OptionUpdateRequestDto {

    @Schema(example = "시럽 추가")
    @NotBlank
    @NotNull(message = "optionNameKr 값은 필수입니다.")
    private String optionNameKr;

    @Schema(example = "syrup")
    @NotBlank
    @NotNull(message = "optionNameEn 값은 필수입니다.")
    private String optionNameEn;

    @Schema(example = "REGISTERED")
    @NotNull(message = "status 값은 필수입니다.")
    @NotBlank
    private String status;
}
