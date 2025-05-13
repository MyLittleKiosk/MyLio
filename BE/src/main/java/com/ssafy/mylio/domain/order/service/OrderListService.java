package com.ssafy.mylio.domain.order.service;

import com.ssafy.mylio.domain.order.dto.response.OrderListResponseDto;
import com.ssafy.mylio.domain.order.entity.Orders;
import com.ssafy.mylio.domain.order.repository.OrdersRepository;
import com.ssafy.mylio.global.common.CustomPage;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

@Service
@RequiredArgsConstructor
public class OrderListService {

    private final OrdersRepository ordersRepository;

    public CustomPage<OrderListResponseDto> getOrderList(Integer storeId, LocalDate startDate, LocalDate endDate, Pageable pageable) {
        LocalDateTime from = (startDate == null) ? null : startDate.atStartOfDay();
        LocalDateTime to = (endDate == null) ? null : endDate.atTime(LocalTime.MAX);

        Page<Orders> orderList = ordersRepository.findByOptionalStoreIdAndOptionalPeriod(storeId, from, to, pageable);
        return new CustomPage<>(orderList.map(OrderListResponseDto::of));
    }



}
