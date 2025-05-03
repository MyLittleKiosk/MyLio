package com.ssafy.mylio.domain.sales.repository;

import com.ssafy.mylio.domain.sales.entity.MonthlySalesSummary;
import com.ssafy.mylio.domain.store.entity.Store;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface MonthlySalesSummaryRepository extends JpaRepository<MonthlySalesSummary, Integer> {
    List<MonthlySalesSummary> findByStoreIdAndYear(int storeId, int year);
}
