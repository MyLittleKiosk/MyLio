package com.ssafy.mylio.domain.sales.service;

import com.ssafy.mylio.domain.order.entity.Orders;
import com.ssafy.mylio.domain.order.repository.OrdersRepository;
import com.ssafy.mylio.domain.payment.entity.PaymentMethod;
import com.ssafy.mylio.domain.sales.entity.MonthlyPaymentMethodRatio;
import com.ssafy.mylio.domain.sales.entity.YearlyPaymentMethodRatio;
import com.ssafy.mylio.domain.sales.repository.MonthlyPaymentMethodRatioRepository;
import com.ssafy.mylio.domain.sales.repository.YearlyPaymentMethodRatioRepository;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.YearMonth;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class PaymentSalesService {

    private final StoreRepository storeRepository;
    private final OrdersRepository ordersRepository;
    private final MonthlyPaymentMethodRatioRepository monthlyPaymentRepository;
    private final YearlyPaymentMethodRatioRepository yearlyPaymentRepository;

    @Transactional
    public void createPaymentSales(LocalDate date){
        // store 정보 조회
        List<Store> storeList = storeRepository.findAll();

        for(Store store : storeList){
            createMonthlyPaymentSales(store, date); // 월별 통계 생성
            createYearlyPaymentSales(store, date); // 연도별 통계 생성
        }
    }

    private void createMonthlyPaymentSales(Store store, LocalDate date){

        YearMonth ym = YearMonth.from(date);
        LocalDate start = ym.atDay(1);
        LocalDate end = ym.atEndOfMonth();

        // 해당 월의 모든 일별 통계 조회
        List<Orders> orders = ordersRepository.findByStoreIdAndCreatedAtBetween(
                store.getId(),
                start.atStartOfDay(),
                end.plusDays(1).atStartOfDay());
        if (orders.isEmpty()) return;  // 매출 데이터 없으면 종료

        // 결제수단별 매출 합계 맵 계산
        Map<PaymentMethod, BigDecimal> byMethod = orders.stream()
                .collect(Collectors.groupingBy(
                        Orders::getPaymentMethod,
                        Collectors.mapping(
                                o -> BigDecimal.valueOf(o.getTotalPrice()),
                                Collectors.reducing(BigDecimal.ZERO, BigDecimal::add)
                        )
                ));

        // 전체 매출 합계
        BigDecimal total = byMethod.values().stream().reduce(BigDecimal.ZERO, BigDecimal::add);

        List<MonthlyPaymentMethodRatio> stats = byMethod.entrySet().stream()
                .map(e -> MonthlyPaymentMethodRatio.builder()
                        .store(store)
                        .method(e.getKey())
                        .year(ym.getYear())
                        .month(ym.getMonthValue())
                        .ratio(
                                // 소수점 넷째 자리 반올림 후 100배
                                e.getValue()
                                        .divide(total, 4, RoundingMode.HALF_UP)
                                        .multiply(BigDecimal.valueOf(100))
                        )
                        .build()
                )
                .collect(Collectors.toList());

        //기존 같은 연·월 데이터 삭제 후 저장
        monthlyPaymentRepository.deleteByStoreAndYearAndMonth(store,  ym.getYear(), ym.getMonthValue());
        monthlyPaymentRepository.saveAll(stats);

    }

    private void createYearlyPaymentSales(Store store, LocalDate date){
        int year = date.getYear();
        LocalDate start = LocalDate.of(year, 1, 1);
        LocalDate end   = LocalDate.of(year, 12, 31);

        // 해당 월의 모든 일별 통계 조회
        List<Orders> orders = ordersRepository.findByStoreIdAndCreatedAtBetween(
                store.getId(),
                start.atStartOfDay(),
                end.plusDays(1).atStartOfDay());
        if (orders.isEmpty()) return;  // 매출 데이터 없으면 종료

        // 결제수단별 매출 합계 맵 계산
        Map<PaymentMethod, BigDecimal> byMethod = orders.stream()
                .collect(Collectors.groupingBy(
                        Orders::getPaymentMethod,
                        Collectors.mapping(
                                o -> BigDecimal.valueOf(o.getTotalPrice()),
                                Collectors.reducing(BigDecimal.ZERO, BigDecimal::add)
                        )
                ));

        // 전체 매출 합계
        BigDecimal total = byMethod.values().stream().reduce(BigDecimal.ZERO, BigDecimal::add);

        List<YearlyPaymentMethodRatio> stats = byMethod.entrySet().stream()
                .map(e -> YearlyPaymentMethodRatio.builder()
                        .store(store)
                        .method(e.getKey())
                        .year(year)
                        .ratio(
                                e.getValue()
                                        .divide(total, 4, RoundingMode.HALF_UP)
                                        .multiply(BigDecimal.valueOf(100))
                        )
                        .build()
                )
                .collect(Collectors.toList());

        //기존 같은 년도 데이터 삭제 후 저장
        yearlyPaymentRepository.deleteByStoreAndYear(store, year);
        yearlyPaymentRepository.saveAll(stats);
    }

}
