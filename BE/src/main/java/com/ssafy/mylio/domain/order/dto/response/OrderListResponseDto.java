package com.ssafy.mylio.domain.order.dto.response;

import com.ssafy.mylio.domain.order.entity.Orders;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;
import lombok.experimental.SuperBuilder;

import java.time.LocalDateTime;


@Getter
@SuperBuilder
public class OrderListResponseDto {

    @Schema(example = "1")
    private Integer orderId;

    @Schema(example = "2023-04-22 14:30")
    private LocalDateTime orderedAt;

    @Schema(example = "15500")
    private Integer totalPrice;

    @Schema(example = "매장")
    private String orderType;

    @Schema(example = "신용카드")
    private String paidBy;

    public static OrderListResponseDto of(Orders order){
        return OrderListResponseDto.builder()
                .orderId(order.getId())
                .orderedAt(order.getCreatedAt())
                .totalPrice(order.getTotalPrice())
                .orderType(order.getIsToGo() ? "포장" : "매장")
                .paidBy(order.getPaymentMethod().getDescription())
                .build();
    }

}
