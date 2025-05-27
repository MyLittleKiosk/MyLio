package com.ssafy.mylio.domain.order.repository;

import com.ssafy.mylio.domain.order.entity.OrderItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.time.LocalDateTime;
import java.util.List;

public interface OrderItemRepository extends JpaRepository<OrderItem, Integer> {

    /**
     * 매장(storeId)의 주문 아이템을, createdAt이
     * [date 00:00:00, date+1 00:00:00) 범위에 있는 것만 조회.
     * Menu와 Category를 fetch join 해서 한 번에 로드.
     */
    @Query("SELECT oi " +
            "FROM OrderItem oi " +
            " JOIN FETCH oi.menu m " +
            " JOIN FETCH m.category c " +
            " JOIN oi.order o " +
            "WHERE o.store.id = :storeId " +
            "  AND oi.createdAt >= :start " +
            "  AND oi.createdAt < :end")
    List<OrderItem> findByStoreAndCreatedAtBetween(
            @Param("storeId") Integer storeId,
            @Param("start") LocalDateTime start,
            @Param("end") LocalDateTime end
    );

    @Query("SELECT oi " +
            "FROM OrderItem oi " +
            "WHERE oi.order.id = :orderId")
    List<OrderItem> findAllByOrderId(@Param("orderId") Integer orderId);

}