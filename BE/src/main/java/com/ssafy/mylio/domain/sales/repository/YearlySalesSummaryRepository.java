package com.ssafy.mylio.domain.sales.repository;

import com.ssafy.mylio.domain.sales.entity.YearlySalesSummary;
import com.ssafy.mylio.domain.store.entity.Store;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface YearlySalesSummaryRepository extends JpaRepository<YearlySalesSummary, Integer> {
    /** 해당 매장·연도의 월별 기록 삭제 */
    void deleteByStoreAndYear(Store store, int year);
}
