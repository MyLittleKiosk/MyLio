package com.ssafy.mylio.domain.kiosk.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Getter;

@Getter
public class KioskCreateRequestDto {
    @Schema(example = "키오스크 01")
    @NotBlank(message = "키오스크 이름은 필수값입니다.")
    private String name;

    @Schema(example = "A")
    @NotBlank(message = "주문 시작번호는 필수값입니다.")
    private String startOrder;
}
