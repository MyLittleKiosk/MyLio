package com.ssafy.mylio.domain.sales.repository;

import com.ssafy.mylio.domain.sales.entity.DailySalesSummary;
import com.ssafy.mylio.domain.store.entity.Store;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;

@Repository
public interface DailySalesSummaryRepository extends JpaRepository<DailySalesSummary, Integer> {
    void deleteByStoreAndStatDate(Store store, LocalDate statDate);
}
