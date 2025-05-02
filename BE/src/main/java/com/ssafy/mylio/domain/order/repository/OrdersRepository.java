package com.ssafy.mylio.domain.order.repository;

import com.ssafy.mylio.domain.order.entity.Orders;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface OrdersRepository extends JpaRepository<Orders, Integer> {
    List<Orders> findByStoreIdAndCreatedAtBetween(Integer storeId, LocalDateTime start, LocalDateTime end);
}
