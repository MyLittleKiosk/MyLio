package com.ssafy.mylio.domain.sales.service;

import com.ssafy.mylio.domain.category.entity.Category;
import com.ssafy.mylio.domain.order.entity.OrderItem;
import com.ssafy.mylio.domain.order.repository.OrderItemRepository;
import com.ssafy.mylio.domain.sales.entity.MonthlyCategorySalesRatio;
import com.ssafy.mylio.domain.sales.entity.YearlyCategorySalesRatio;
import com.ssafy.mylio.domain.sales.repository.MonthlyCategorySalesRatioRepository;
import com.ssafy.mylio.domain.sales.repository.YearlyCategorySalesRatioRepository;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.YearMonth;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;


@Service
@RequiredArgsConstructor
public class CategorySalesService {

    private final OrderItemRepository orderItemRepository;
    private final StoreRepository storeRepository;
    private final MonthlyCategorySalesRatioRepository monthlyCategoryRepository;
    private final YearlyCategorySalesRatioRepository yearlyCategoryRepository;

    @Transactional
    public void createCategorySales(LocalDate date){
        // Store 정보 조회
        List<Store> storeList = storeRepository.findAll();
        
       for(Store store : storeList){
           // 월별 통계 생성
           createMonthlyCategorySales(store, date);
           // 연도별 통계 생성
           createYearlyCategorySales(store, date);
       }
    }

    private void createMonthlyCategorySales(Store store, LocalDate date) {
        YearMonth ym = YearMonth.from(date);
        LocalDate start = ym.atDay(1);
        LocalDate end = ym.atEndOfMonth();

        // 해당 월의 모든 일별 통계 조회
        List<OrderItem> items = orderItemRepository.findByStoreAndCreatedAtBetween(
                store.getId(),
                start.atStartOfDay(),
                end.plusDays(1).atStartOfDay()
        );
        if (items.isEmpty()) return;  // 매출 데이터 없으면 종료

        // 카테고리별 매출 합계 계산
        Map<Category, BigDecimal> byCategory = getAmountByCategory(items);
        // 전체 매출 합계
        BigDecimal total = getTotal(byCategory);

        // 비율 계산 후 엔티티 리스트 생성
        List<MonthlyCategorySalesRatio> stats = byCategory.entrySet().stream()
                .map(e -> MonthlyCategorySalesRatio.builder()
                        .store(store)
                        .category(e.getKey())
                        .year(ym.getYear())
                        .month(ym.getMonthValue())
                        .ratio(calcRatio(e.getValue(), total))
                        .build()
                )
                .collect(Collectors.toList());

        // 기존 같은 연월 데이터 삭제 후 저장
        monthlyCategoryRepository.deleteByStoreAndYearAndMonth(store, ym.getYear(), ym.getMonthValue());
        monthlyCategoryRepository.saveAll(stats);
    }

    private void createYearlyCategorySales(Store store, LocalDate date) {
        int year = date.getYear();
        LocalDate start = LocalDate.of(year, 1, 1);
        LocalDate end   = LocalDate.of(year, 12, 31);

        // 해당 년도의 모든 일별 통계 조회
        List<OrderItem> items = orderItemRepository.findByStoreAndCreatedAtBetween(
                store.getId(),
                start.atStartOfDay(),
                end.plusDays(1).atStartOfDay()
        );
        if (items.isEmpty()) return;

        // 카테고리별 매출 합계 계산
        Map<Category, BigDecimal> byCategory = getAmountByCategory(items);
        // 전체 매출 합계
        BigDecimal total = getTotal(byCategory);

        List<YearlyCategorySalesRatio> stats = byCategory.entrySet().stream()
                .map(e -> YearlyCategorySalesRatio.builder()
                        .store(store)
                        .category(e.getKey())
                        .year(year)
                        .ratio(calcRatio(e.getValue(), total))
                        .build()
                )
                .collect(Collectors.toList());

        yearlyCategoryRepository.deleteByStoreAndYear(store, year);
        yearlyCategoryRepository.saveAll(stats);
    }


    /**
     * Map에 담긴 모든 카테고리 매출 금액을 합산하여 전체 매출 구하기
     * @param byCategory 카테고리별 매출 합계 맵
     * @return 전체 매출 합계
     */
    private BigDecimal getTotal(Map<Category, BigDecimal> byCategory) {
        return byCategory.values().stream()
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    /**
     * OrderItem 리스트에서 카테고리별 매출 합계를 계산하여 Map으로 반환
     * @param items 조회된 주문 아이템 리스트
     * @return 카테고리 키, 해당 카테고리 매출 합계 값
     */
    private Map<Category, BigDecimal> getAmountByCategory(List<OrderItem> items) {
        Map<Category, BigDecimal> map = new HashMap<>();

        for(OrderItem orderItem : items){
            BigDecimal amount = BigDecimal.valueOf(orderItem.getPrice());
            Category category = orderItem.getMenu().getCategory();

            // 같은 카테고리가 있으면 더하고, 없으면 새로 넣기
            map.merge(category, amount, BigDecimal::add);
        }
        return map;
    }

    /**
     * 전체 매출 대비 특정 카테고리 매출 비율 계산 (백분율)
     * @param amount  특정 카테고리 매출
     * @param total   전체 매출
     * @return        비율(%), 소수점 넷째자리까지 계산 후 반올림
     */
    private BigDecimal calcRatio(BigDecimal amount, BigDecimal total) {
        // 전체 매출이 0이면 비율 0으로 처리
        if (total.compareTo(BigDecimal.ZERO) == 0) {
            return BigDecimal.ZERO;
        }
        // (amount / total) → 소수점 4자리 반올림 → 100 곱해서 %
        return amount.divide(total, 4, RoundingMode.HALF_UP)
                .multiply(BigDecimal.valueOf(100));
    }

}