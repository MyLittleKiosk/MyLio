package com.ssafy.mylio.domain.sales.repository;

import com.ssafy.mylio.domain.sales.entity.YearlyCategorySalesRatio;
import com.ssafy.mylio.domain.store.entity.Store;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface YearlyCategorySalesRatioRepository extends JpaRepository<YearlyCategorySalesRatio, Integer> {
    // 해당 매장·연도의 모든 통계 레코드 삭제
    void deleteByStoreAndYear(Store store, int year);

    // 연도별 통계 조회
    List<YearlyCategorySalesRatio> findByStoreIdAndYear(Integer storeId, int year);
}
