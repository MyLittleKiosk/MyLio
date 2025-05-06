package com.ssafy.mylio.domain.order.repository;

import com.ssafy.mylio.domain.order.entity.Orders;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.time.LocalDate;
public interface OrderRepository extends JpaRepository<Orders, Integer> {

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