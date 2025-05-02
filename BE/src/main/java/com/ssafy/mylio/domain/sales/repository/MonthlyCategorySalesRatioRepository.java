package com.ssafy.mylio.domain.sales.repository;

import com.ssafy.mylio.domain.sales.entity.MonthlyCategorySalesRatio;
import com.ssafy.mylio.domain.store.entity.Store;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface MonthlyCategorySalesRatioRepository  extends JpaRepository<MonthlyCategorySalesRatio, Integer> {

    // 해당 매장·연도·월의 모든 통계 레코드 삭제
    void deleteByStoreAndYearAndMonth(Store store, int year, int month);
}
