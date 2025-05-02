package com.ssafy.mylio.domain.sales.repository;

import com.ssafy.mylio.domain.sales.entity.YearlyCategorySalesRatio;
import com.ssafy.mylio.domain.store.entity.Store;
import org.springframework.data.jpa.repository.JpaRepository;

public interface YearlyCategorySalesRatioRepository extends JpaRepository<YearlyCategorySalesRatio, Integer> {
    // 해당 매장·연도의 모든 통계 레코드 삭제
    void deleteByStoreAndYear(Store store, int year);
}
