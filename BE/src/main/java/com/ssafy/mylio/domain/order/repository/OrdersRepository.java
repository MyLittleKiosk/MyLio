package com.ssafy.mylio.domain.order.repository;

import com.ssafy.mylio.domain.order.entity.Orders;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface OrdersRepository extends JpaRepository<Orders, Integer> {
    List<Orders> findByStoreIdAndCreatedAtBetween(Integer storeId, LocalDateTime start, LocalDateTime end);

    /**
     * 특정 매장(storeId)의 합계를 createdAt(LocalDateTime) 범위 [start, end) 내에서 계산
     */
    @Query("SELECT SUM(o.totalPrice) FROM Orders o " +
            " WHERE o.store.id = :storeId " +
            "   AND o.createdAt >= :start " +
            "   AND o.createdAt <  :end")
    Integer sumTotalPriceByStoreIdAndCreatedAtBetween(
            @Param("storeId") Integer storeId,
            @Param("start")   LocalDateTime start,
            @Param("end")     LocalDateTime end
    );

    @Query("""
        SELECT COALESCE(SUM(o.totalPrice), 0) 
        FROM Orders o 
        WHERE o.store.id = :storeId 
        AND DATE(o.createdAt) = CURRENT_DATE
    """)
    Integer getTodayTotalSales(@Param("storeId") Integer storeId);

    @Query("""
        SELECT COUNT(o) 
        FROM Orders o 
        WHERE o.store.id = :storeId 
        AND DATE(o.createdAt) = CURRENT_DATE
    """)
    Integer getTodayOrderCount(@Param("storeId") Integer storeId);
}
