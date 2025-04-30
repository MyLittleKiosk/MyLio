package com.ssafy.mylio.domain.options.dto.request;

import com.ssafy.mylio.domain.options.entity.OptionDetail;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import javax.validation.constraints.NotNull;

@Getter
@Builder
public class OptionDetailRequestDto {

    @Schema(example = "아몬드 우유")
    @NotNull(message = "value값은 필수입니다.")
    private String value;

    @Schema(example = "500")
    @NotNull(message = "additional_price는 필수입니다.")
    private Integer additionalPrice;

    public OptionDetail toEntity(){
        return OptionDetail.builder()
                .value(this.value)
                .additionalPrice(this.additionalPrice)
                .build();
    }
}
