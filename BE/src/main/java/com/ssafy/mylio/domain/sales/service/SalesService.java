package com.ssafy.mylio.domain.sales.service;

import com.ssafy.mylio.domain.sales.dto.request.CategorySalesResponseDto;
import com.ssafy.mylio.domain.sales.entity.MonthlyCategorySalesRatio;
import com.ssafy.mylio.domain.sales.entity.YearlyCategorySalesRatio;
import com.ssafy.mylio.domain.sales.repository.MonthlyCategorySalesRatioRepository;
import com.ssafy.mylio.domain.sales.repository.YearlyCategorySalesRatioRepository;
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

}
