package com.ssafy.mylio.domain.sales.repository;

import com.ssafy.mylio.domain.sales.entity.YearlyDineinTakeoutRatio;
import com.ssafy.mylio.domain.store.entity.Store;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface YearlyDineInTakeoutRatioRepository extends JpaRepository<YearlyDineinTakeoutRatio, Integer> {
    // 해당 매장·연도의 모든 통계 레코드 삭제
    void deleteByStoreAndYear(Store store, int year);
    // 연도별 통계 조회
    List<YearlyDineinTakeoutRatio> findByStoreIdAndYear(Integer storeId, int year);
}
