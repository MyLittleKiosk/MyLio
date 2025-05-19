package com.ssafy.mylio.domain.order.controller;


import com.ssafy.mylio.domain.order.dto.response.OrderDetailResponseDto;
import com.ssafy.mylio.domain.order.dto.response.OrderListResponseDto;
import com.ssafy.mylio.domain.order.service.OrderListService;
import com.ssafy.mylio.global.aop.swagger.ApiErrorCodeExamples;
import com.ssafy.mylio.global.common.CustomPage;
import com.ssafy.mylio.global.common.response.CommonResponse;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import com.ssafy.mylio.global.util.AuthenticationUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;

@RestController
@RequiredArgsConstructor
@RequestMapping("/order_list")
@Slf4j
@Tag(name = "주문 관리", description = "주문 목록 조회, 주문 상세 조회 api")
public class OrderListController {

    private final OrderListService orderListService;
    private final AuthenticationUtil authenticationUtil;

    @GetMapping
    @Operation(summary = "주문 목록 조회", description = "전체 주문 목록을 조회합니다")
    public ResponseEntity<CommonResponse<CustomPage<OrderListResponseDto>>> getOrderList(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestParam(name="startDate", required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam(name="endDate", required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate,
            @PageableDefault(sort = "createdAt", direction = Sort.Direction.DESC) Pageable pageable
          )
    {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        return CommonResponse.ok(orderListService.getOrderList(storeId, startDate, endDate, pageable));
    }

    @GetMapping("/{orderId}")
    @Operation(summary = "주문 상세 조회", description = "주문의 상세 내용을 조회합니다")
    @ApiErrorCodeExamples({ErrorCode.ORDER_NOT_FOUND})
    public ResponseEntity<CommonResponse<OrderDetailResponseDto>> getOrderDetail(
            @PathVariable("orderId") Integer orderId)
    {
        return CommonResponse.ok(orderListService.getOrderDetail(orderId));
    }

}
