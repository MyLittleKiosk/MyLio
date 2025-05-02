package com.ssafy.mylio.domain.sales.repository;

import com.ssafy.mylio.domain.sales.entity.MonthlySalesSummary;
import com.ssafy.mylio.domain.store.entity.Store;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface MonthlySalesSummaryRepository extends JpaRepository<MonthlySalesSummary, Integer> {
    /** 해당 매장·연도·월의 월별 기록 삭제 */
    void deleteByStoreAndYearAndMonth(Store store, int year, int month);
}
