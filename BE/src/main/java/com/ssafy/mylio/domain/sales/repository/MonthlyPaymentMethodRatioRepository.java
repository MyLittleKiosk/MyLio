package com.ssafy.mylio.domain.sales.repository;

import com.ssafy.mylio.domain.sales.entity.MonthlyPaymentMethodRatio;
import com.ssafy.mylio.domain.store.entity.Store;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface MonthlyPaymentMethodRatioRepository extends JpaRepository<MonthlyPaymentMethodRatio, Integer> {
    // 해당 매장·연도·월의 모든 통계 레코드 삭제
    void deleteByStoreAndYearAndMonth(Store store, int year, int month);
    // 월별 통계 조회
    List<MonthlyPaymentMethodRatio> findByStoreIdAndYearAndMonth(Integer storeId, int year, int month);
}
