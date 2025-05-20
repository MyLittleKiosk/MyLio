package com.ssafy.mylio.domain.order.dto.response;

import com.ssafy.mylio.domain.order.entity.Orders;
import lombok.Getter;
import lombok.experimental.SuperBuilder;
import java.util.List;

@Getter
@SuperBuilder
public class OrderDetailResponseDto extends OrderListResponseDto{

    private List<OrderItemResponseDto> orderItems;

    public static OrderDetailResponseDto of(Orders order, List<OrderItemResponseDto> orderItems){
        return OrderDetailResponseDto.builder()
                .orderId(order.getId())
                .orderedAt(order.getCreatedAt())
                .totalPrice(order.getTotalPrice())
                .orderType(order.getIsToGo() ? "포장" : "매장")
                .paidBy(order.getPaymentMethod().getDescription())
                .orderItems(orderItems)
                .build();
    }

}
