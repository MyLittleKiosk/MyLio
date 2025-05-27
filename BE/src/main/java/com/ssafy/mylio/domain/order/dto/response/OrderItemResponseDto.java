package com.ssafy.mylio.domain.order.dto.response;

import com.ssafy.mylio.domain.order.entity.OrderItem;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Builder
@Getter
public class OrderItemResponseDto {

    @Schema(example = "아메리카노")
    private String itemName;

    @Schema(example = "1")
    private Integer quantity;

    @Schema(example = "15000")
    private Integer price;

    @Schema(example = "[ICE, 샷 추가]")
    List<String> options;

    public static OrderItemResponseDto of(OrderItem orderItem, List<String> options){
       return OrderItemResponseDto.builder()
                .itemName(orderItem.getMenu().getNameKr())
                .quantity(orderItem.getQuantity())
                .price(orderItem.getPrice())
                .options(options)
                .build();
    }

}
