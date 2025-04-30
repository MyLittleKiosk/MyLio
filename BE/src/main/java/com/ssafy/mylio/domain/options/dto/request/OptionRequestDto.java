package com.ssafy.mylio.domain.options.dto.request;

import com.ssafy.mylio.domain.options.entity.Options;
import com.ssafy.mylio.domain.store.entity.Store;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import javax.validation.constraints.NotNull;

@Getter
@Builder
public class OptionRequestDto {

    @Schema(example = "토핑 추가")
    @NotNull(message = "value값은 필수입니다.")
    private String optionNameKr;

    @Schema(example = "topping")
    @NotNull(message = "value값은 필수입니다.")
    private String optionNameEn;

    public Options toEntity(Store store){
        return Options.builder()
                .store(store)
                .optionNameKr(this.optionNameKr)
                .optionNameEn(this.optionNameEn)
                .build();
    }
}
