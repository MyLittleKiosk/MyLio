package com.ssafy.mylio.domain.sales.repository;

import com.ssafy.mylio.domain.sales.entity.DailySalesSummary;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface DailySalesSummaryRepository  extends JpaRepository<DailySalesSummary, Integer> {
    @Query("""
        SELECT d FROM DailySalesSummary d 
        WHERE d.store.id = :storeId 
        AND FUNCTION('YEAR', d.statDate) = :year 
        AND FUNCTION('MONTH', d.statDate) = :month
    """)
    List<DailySalesSummary> findByStoreIdAndYearAndMonth(
            @Param("storeId") int storeId,
            @Param("year") int year,
            @Param("month") int month
    );}
