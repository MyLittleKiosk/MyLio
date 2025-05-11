package com.ssafy.mylio.domain.sales.service;

import com.ssafy.mylio.domain.order.repository.OrdersRepository;
import com.ssafy.mylio.domain.sales.entity.DailySalesSummary;
import com.ssafy.mylio.domain.sales.entity.MonthlySalesSummary;
import com.ssafy.mylio.domain.sales.entity.YearlySalesSummary;
import com.ssafy.mylio.domain.sales.repository.DailySalesSummaryRepository;
import com.ssafy.mylio.domain.sales.repository.MonthlySalesSummaryRepository;
import com.ssafy.mylio.domain.sales.repository.YearlySalesSummaryRepository;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.YearMonth;
import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class TotalSalesService {

    private final StoreRepository storeRepository;
    private final OrdersRepository ordersRepository;
    private final DailySalesSummaryRepository dailySalesSummaryRepository;
    private final MonthlySalesSummaryRepository monthlySalesSummaryRepository;
    private final YearlySalesSummaryRepository yearlySalesSummaryRepository;

    @Transactional
    public void createSalesSummary(LocalDate date){
        // 1) 모든 매장 조회
        List<Store> stores = storeRepository.findAll();

        for (Store store : stores) {
            createDailySalesSummary(store, date);
            createMonthlySalesSummary(store, date);
            createYearlySalesSummary(store, date);
        }

    }

    private void createDailySalesSummary(Store store, LocalDate date) {
        LocalDateTime start = date.atStartOfDay();
        LocalDateTime end   = date.plusDays(1).atStartOfDay();

        // 주문매출 합계 조회
        Integer total = ordersRepository.sumTotalPriceByStoreIdAndCreatedAtBetween(store.getId(), start, end);
        int totalSales = total == null ? 0 : total;

        // 기존 일별 기록 삭제 (중복 방지)
        dailySalesSummaryRepository.deleteByStoreAndStatDate(store, date);
        
        // 엔티티 저장
        DailySalesSummary dailySalesSummary = DailySalesSummary.builder()
                .store(store)
                .statDate(date)
                .totalSales(totalSales)
                .build();

        dailySalesSummaryRepository.save(dailySalesSummary);
    }

    private void createMonthlySalesSummary(Store store, LocalDate date) {
        YearMonth ym = YearMonth.from(date);
        LocalDateTime start = ym.atDay(1).atStartOfDay();
        LocalDateTime end   = ym.plusMonths(1).atDay(1).atStartOfDay();

        // 주문매출 합계 조회
        Integer total = ordersRepository.sumTotalPriceByStoreIdAndCreatedAtBetween(store.getId(), start, end);
        int totalSales = total == null ? 0 : total;

        // 기존 월별 기록 삭제 (중복 방지)
        monthlySalesSummaryRepository.deleteByStoreAndYearAndMonth(store, ym.getYear(), ym.getMonthValue());

        // 엔티티 저장
        MonthlySalesSummary monthlySalesSummary = MonthlySalesSummary.builder()
                .store(store)
                .year(ym.getYear())
                .month(ym.getMonthValue())
                .totalSales(totalSales)
                .build();

        monthlySalesSummaryRepository.save(monthlySalesSummary);
    }


    private void createYearlySalesSummary(Store store, LocalDate date) {
        int year = date.getYear();
        LocalDateTime start = LocalDate.of(year, 1, 1).atStartOfDay();
        LocalDateTime end   = LocalDate.of(year + 1, 1, 1).atStartOfDay();

        // 주문매출 합계 조회
        Integer total = ordersRepository.sumTotalPriceByStoreIdAndCreatedAtBetween(store.getId(), start, end);
        int totalSales = total == null ? 0 : total;

        // 기존 연도별 기록 삭제 (중복 방지)
        yearlySalesSummaryRepository.deleteByStoreAndYear(store, year);

        // 엔티티 저장
        YearlySalesSummary yearlySalesSummary = YearlySalesSummary.builder()
                .store(store)
                .year(year)
                .totalSales(totalSales)
                .build();

        yearlySalesSummaryRepository.save(yearlySalesSummary);

    }
}
