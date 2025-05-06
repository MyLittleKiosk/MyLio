package com.ssafy.mylio.domain.sales.service;

import com.ssafy.mylio.domain.sales.dto.response.*;
import com.ssafy.mylio.domain.account.entity.AccountRole;
import com.ssafy.mylio.domain.order.repository.OrderRepository;
import com.ssafy.mylio.domain.sales.entity.MonthlyCategorySalesRatio;
import com.ssafy.mylio.domain.sales.entity.YearlyCategorySalesRatio;
import com.ssafy.mylio.domain.sales.repository.*;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class SalesService {

    private final StoreRepository storeRepository;
    private final MonthlyCategorySalesRatioRepository monthlyCategorySalesRatioRepository;
    private final YearlyCategorySalesRatioRepository yearlyCategorySalesRatioRepository;
    private final MonthlySalesSummaryRepository monthlySalesRepo;
    private final DailySalesSummaryRepository dailySalesRepo;
    private final OrderRepository orderRepository;
    private final MonthlyPaymentMethodRatioRepository monthlyPaymentMethodRatioRepository;
    private final YearlyPaymentMethodRatioRepository yearlyPaymentMethodRatioRepository;
    private final MonthlyDineInTakeoutRatioRepository monthlyDineInTakeoutRatioRepository;
    private final YearlyDineInTakeoutRatioRepository yearlyDineInTakeoutRatioRepository;
    public CategorySalesResponseDto getCategorySales(Integer storeId, Integer year, Integer month){
        Store store = getStore(storeId);

        List<CategorySalesResponseDto.CategoryRatioDto> ratios;

        if (month != null) {
            // 월별 엔티티에서 조회
            List<MonthlyCategorySalesRatio> list =
                    monthlyCategorySalesRatioRepository.findByStoreIdAndYearAndMonth(storeId, year, month);
            ratios = list.stream()
                    .map(e -> CategorySalesResponseDto.CategoryRatioDto.of(
                            e.getCategory().getNameKr(),
                            e.getRatio()
                    ))
                    .collect(Collectors.toList());
        } else {
            // 연도별 엔티티에서 조회
            List<YearlyCategorySalesRatio> list =
                    yearlyCategorySalesRatioRepository.findByStoreIdAndYear(storeId, year);
            ratios = list.stream()
                    .map(e -> CategorySalesResponseDto.CategoryRatioDto.of(
                            e.getCategory().getNameKr(),
                            e.getRatio()
                    ))
                    .collect(Collectors.toList());
        }

        return CategorySalesResponseDto.builder()
                .ratioByCategory(ratios)
                .build();
    }

    private Store getStore(Integer storeId) {
        return  storeRepository.findById(storeId)
                .orElseThrow(() -> new CustomException(ErrorCode.STORE_NOT_FOUND, "storeId", storeId));
    }

    public List<SalesResponse> getSalesStatistics(String userType, int storeId, int year, Integer month){
        //역할이 STORE가 아니면 불가
        if (!userType.equals(AccountRole.STORE.getCode())) {
            throw new CustomException(ErrorCode.INVALID_ROLE)
                    .addParameter("userType",userType);
        }

        //월이 없으면 년도 조회
        if(month == null){
            return monthlySalesRepo.findByStoreIdAndYear(storeId, year).stream()
                    .map(e -> SalesResponse.builder()
                            .type(e.getMonth())       // 1~12
                            .total(e.getTotalSales())
                            .build())
                    .toList();
        }
        //월별 조회
        return dailySalesRepo.findByStoreIdAndYearAndMonth(storeId, year, month).stream()
                .map(e -> SalesResponse.builder()
                        .type(e.getStatDate().getDayOfMonth()) // 1~31
                        .total(e.getTotalSales())
                        .build())
                .toList();
    }

    public DailySalesResponseDto getDailySales(Integer storeId, String userType){
        //역할이 STORE가 아니면 불가
        if (!userType.equals(AccountRole.STORE.getCode())) {
            throw new CustomException(ErrorCode.INVALID_ROLE)
                    .addParameter("userType",userType);
        }

        Integer totalSales = orderRepository.getTodayTotalSales(storeId);
        Integer totalOrders = orderRepository.getTodayOrderCount(storeId);

        return DailySalesResponseDto.of(totalSales, totalOrders);

    }

    public List<PaymentSalesResponseDto> getPaymentMethodRatio(String userType ,Integer storeId, Integer year, Integer month) {
        //역할이 STORE가 아니면 불가
        if (!userType.equals(AccountRole.STORE.getCode())) {
            throw new CustomException(ErrorCode.INVALID_ROLE)
                    .addParameter("userType",userType);
        }

        if (month != null) {
            // 월별 결제 수단 비율
            return monthlyPaymentMethodRatioRepository.findByStoreIdAndYearAndMonth(storeId, year, month).stream()
                    .map(e -> PaymentSalesResponseDto.of(e.getMethod().getDescription(), e.getRatio()))
                    .toList();
        } else {
            // 연도별 결제 수단 비율
            return yearlyPaymentMethodRatioRepository.findByStoreIdAndYear(storeId, year).stream()
                    .map(e -> PaymentSalesResponseDto.of(e.getMethod().getDescription(), e.getRatio()))
                    .toList();
        }
    }

    public List<OrderTypeSalesResponseDto> getOrderTypeStatics(String userType, Integer storeId, Integer year, Integer month){
        //역할이 STORE가 아니면 불가
        if (!userType.equals(AccountRole.STORE.getCode())) {
            throw new CustomException(ErrorCode.INVALID_ROLE)
                    .addParameter("userType",userType);
        }

        if(month != null){
            //월별 결제
            return monthlyDineInTakeoutRatioRepository.findByStoreIdAndYearAndMonth(storeId,year,month).stream()
                    .map(e -> OrderTypeSalesResponseDto.of(e.getType().getDescription(), e.getRatio()))
                    .toList();
        }else{
            //연도별 결제
            return yearlyDineInTakeoutRatioRepository.findByStoreIdAndYear(storeId,year).stream()
                    .map(e -> OrderTypeSalesResponseDto.of(e.getType().getDescription(),  e.getRatio()))
                    .toList();
        }
    }
}
