package com.ssafy.mylio.domain.order.service;

import com.ssafy.mylio.domain.order.dto.response.OrderDetailResponseDto;
import com.ssafy.mylio.domain.order.dto.response.OrderItemResponseDto;
import com.ssafy.mylio.domain.order.dto.response.OrderListResponseDto;
import com.ssafy.mylio.domain.order.entity.OrderItem;
import com.ssafy.mylio.domain.order.entity.Orders;
import com.ssafy.mylio.domain.order.repository.OrderItemOptionRepository;
import com.ssafy.mylio.domain.order.repository.OrderItemRepository;
import com.ssafy.mylio.domain.order.repository.OrdersRepository;
import com.ssafy.mylio.global.common.CustomPage;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class OrderListService {

    private final OrdersRepository ordersRepository;
    private final OrderItemRepository orderItemRepository;
    private final OrderItemOptionRepository orderItemOptionRepository;

    public CustomPage<OrderListResponseDto> getOrderList(Integer storeId, LocalDate startDate, LocalDate endDate, Pageable pageable) {
        LocalDateTime from = (startDate == null) ? null : startDate.atStartOfDay();
        LocalDateTime to = (endDate == null) ? null : endDate.atTime(LocalTime.MAX);

        Page<Orders> orderList = ordersRepository.findByOptionalStoreIdAndOptionalPeriod(storeId, from, to, pageable);
        return new CustomPage<>(orderList.map(OrderListResponseDto::of));
    }

    public OrderDetailResponseDto getOrderDetail(Integer orderId){
        Orders order = getOrder(orderId);
        List<OrderItem> orderItems = orderItemRepository.findAllByOrderId(orderId);
        List<OrderItemResponseDto> orderItemsRes = new ArrayList<>();

        for(OrderItem orderItem : orderItems){

            List<String> optionValues = orderItemOptionRepository.findOptionValuesByOrderItemId(orderItem.getId());
            orderItemsRes.add(OrderItemResponseDto.of(orderItem, optionValues));

        }

        return OrderDetailResponseDto.of(order, orderItemsRes);
    }

    private Orders getOrder(Integer orderId) {
        return  ordersRepository.findById(orderId)
                .orElseThrow(() -> new CustomException(ErrorCode.ORDER_NOT_FOUND, "orderId", orderId));
    }


}
