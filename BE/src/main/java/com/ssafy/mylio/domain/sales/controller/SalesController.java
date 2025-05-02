package com.ssafy.mylio.domain.sales.controller;

import com.ssafy.mylio.domain.sales.dto.request.CategorySalesResponseDto;
import com.ssafy.mylio.domain.sales.service.SalesService;
import com.ssafy.mylio.global.aop.swagger.ApiErrorCodeExamples;
import com.ssafy.mylio.global.common.response.CommonResponse;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import com.ssafy.mylio.global.util.AuthenticationUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/sales")
@RequiredArgsConstructor
@Tag(name = "통계 조회", description = "매출, 카테고리 등의 통계 조회 API")
public class SalesController {

    private final SalesService salesService;
    private final AuthenticationUtil authenticationUtil;

    @GetMapping("/by_category")
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND})
    @Operation(summary = "카테고리 별 매출 통계", description = "카테고리를 기준으로 매출 통계를 조회합니다")
    ResponseEntity<CommonResponse<CategorySalesResponseDto>> getCategoryStatistics(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestParam(value = "year") Integer year,
            @RequestParam(value = "month", required = false) Integer month) {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        return CommonResponse.ok(salesService.getCategorySales(storeId, year, month));
    }
}
