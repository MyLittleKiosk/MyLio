package com.ssafy.mylio.domain.sales.service;

import com.ssafy.mylio.domain.category.entity.Category;
import com.ssafy.mylio.domain.order.entity.OrderItem;
import com.ssafy.mylio.domain.order.entity.OrderStatus;
import com.ssafy.mylio.domain.order.entity.Orders;
import com.ssafy.mylio.domain.order.repository.OrdersRepository;
import com.ssafy.mylio.domain.sales.entity.MonthlyDineinTakeoutRatio;
import com.ssafy.mylio.domain.sales.entity.YearlyDineinTakeoutRatio;
import com.ssafy.mylio.domain.sales.repository.MonthlyDineInTakeoutRatioRepository;
import com.ssafy.mylio.domain.sales.repository.YearlyDineInTakeoutRatioRepository;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.YearMonth;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class OrderTypeSalesService {

    private final StoreRepository storeRepository;
    private final OrdersRepository ordersRepository;
    private final YearlyDineInTakeoutRatioRepository yearOrderTypeRepository;
    private final MonthlyDineInTakeoutRatioRepository monthOrderTypeRepository;

    @Transactional
    public void createOrderTypeSales(LocalDate date) {
        // store 정보 조회
        List<Store> storeList = storeRepository.findAll();

        for (Store store : storeList) {
            createMonthlyOrderTypeSales(store, date);
            createYearlyOrderTypeSales(store, date);
        }

    }

    private void createMonthlyOrderTypeSales(Store store, LocalDate date) {
        YearMonth ym = YearMonth.from(date);
        LocalDate start = ym.atDay(1);
        LocalDate end = ym.atEndOfMonth();

        // 해당 월의 모든 일별 통계 조회
        List<Orders> orders = ordersRepository.findByStoreIdAndCreatedAtBetween(
                store.getId(),
                start.atStartOfDay(),
                end.plusDays(1).atStartOfDay());
        if (orders.isEmpty()) return;  // 매출 데이터 없으면 종료

        // 매장, 포장 별 매출합계 계산
        Map<OrderStatus, BigDecimal> byType = getAmountByOrderStatus(orders);

        // 전체 매출 합계
        BigDecimal total = getTotal(byType);

        // 엔티티 생성
        List<MonthlyDineinTakeoutRatio> stats = byType.entrySet().stream()
                .map(e -> MonthlyDineinTakeoutRatio.builder()
                        .store(store)
                        .year(ym.getYear())
                        .month(ym.getMonthValue())
                        .type(e.getKey())
                        .ratio(
                                total.compareTo(BigDecimal.ZERO) == 0
                                        ? BigDecimal.ZERO
                                        : e.getValue()
                                        .divide(total, 4, RoundingMode.HALF_UP)
                                        .multiply(BigDecimal.valueOf(100))
                        )
                        .build()
                )
                .collect(Collectors.toList());

        monthOrderTypeRepository.deleteByStoreAndYearAndMonth(store, ym.getYear(), ym.getMonthValue());
        monthOrderTypeRepository.saveAll(stats);
    }

    private void createYearlyOrderTypeSales(Store store, LocalDate date) {
        int year = date.getYear();
        LocalDate start = LocalDate.of(year, 1, 1);
        LocalDate end   = LocalDate.of(year, 12, 31);

        // 해당 년도의 모든 일별 통계 조회
        List<Orders> orders = ordersRepository.findByStoreIdAndCreatedAtBetween(
                store.getId(),
                start.atStartOfDay(),
                end.plusDays(1).atStartOfDay()
        );
        if (orders.isEmpty()) return;

        // 매장, 포장 별 매출합계 계산
        Map<OrderStatus, BigDecimal> byType = getAmountByOrderStatus(orders);

        // 전체 매출 합계
        BigDecimal total = getTotal(byType);

        // 엔티티 생성
        List<YearlyDineinTakeoutRatio> stats = byType.entrySet().stream()
                .map(e -> YearlyDineinTakeoutRatio.builder()
                        .store(store)
                        .year(year)
                        .type(e.getKey())
                        .ratio(
                                total.compareTo(BigDecimal.ZERO) == 0
                                        ? BigDecimal.ZERO
                                        : e.getValue()
                                        .divide(total, 4, RoundingMode.HALF_UP)
                                        .multiply(BigDecimal.valueOf(100))
                        )
                        .build()
                )
                .collect(Collectors.toList());

        yearOrderTypeRepository.deleteByStoreAndYear(store, year);
        yearOrderTypeRepository.saveAll(stats);
    }

    /**
     * Map에 담긴 모든 포장/매장 매출 금액을 합산하여 전체 매출 구하기
     * @param byOrderType 포장/매장 매출 합계 맵
     * @return 전체 매출 합계
     */
    private BigDecimal getTotal(Map<OrderStatus, BigDecimal> byOrderType) {
        return byOrderType.values().stream()
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    /**
     * OrderItem 리스트에서 포장/매장 매출 합계를 계산하여 Map으로 반환
     * @param orders 조회된 주문 리스트
     * @return 포장/매장 키, 해당 포장/매장 매출 합계 값
     */
    private Map<OrderStatus, BigDecimal> getAmountByOrderStatus(List<Orders> orders) {
        Map<OrderStatus, BigDecimal> map;

        map = orders.stream()
                .collect(Collectors.groupingBy(
                        o -> o.getIsToGo()
                                ? OrderStatus.TAKEOUT : OrderStatus.DINEIN,
                        Collectors.mapping(
                                o -> BigDecimal.valueOf(o.getTotalPrice()),
                                Collectors.reducing(BigDecimal.ZERO, BigDecimal::add)
                        )
                ));

        return map;
    }
}
