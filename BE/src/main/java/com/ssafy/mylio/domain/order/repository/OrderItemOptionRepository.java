package com.ssafy.mylio.domain.order.repository;

import com.ssafy.mylio.domain.order.entity.OrderItemOption;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface OrderItemOptionRepository extends JpaRepository<OrderItemOption, Integer> {
}
