package com.ssafy.mylio.domain.order.repository;

import com.ssafy.mylio.domain.order.entity.OrderItemOption;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OrderItemOptionRepository extends JpaRepository<OrderItemOption, Integer> {

    @Query("SELECT od.value " +
            "FROM OrderItemOption oio " +
            " JOIN oio.optionDetail od " +
            "WHERE oio.orderItem.id = :orderItemId")
    List<String> findOptionValuesByOrderItemId(@Param("orderItemId") Integer orderItemId);

}
