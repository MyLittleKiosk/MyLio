package com.ssafy.mylio.domain.sales.dto.response;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import java.math.BigDecimal;

@Getter
@Builder
public class PaymentSalesResponseDto {
    @Schema(example = "CARD",description = "결제 방법")
    private String payment_name;

    @Schema(example = "23.93",description = "총 비율")
    private BigDecimal ratio;

    public static PaymentSalesResponseDto of(String payment_name,BigDecimal ratio){
        return PaymentSalesResponseDto.builder()
                .payment_name(payment_name)
                .ratio(ratio)
                .build();
    }
}
