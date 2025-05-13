package com.ssafy.mylio.domain.nutrition.controller;

import com.ssafy.mylio.domain.nutrition.dto.request.NutritionValuePostRequestDto;
import com.ssafy.mylio.domain.nutrition.dto.response.NutritionResponseDto;
import com.ssafy.mylio.domain.nutrition.service.NutritionService;
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

import java.util.List;

@RestController
@RequestMapping("/nutrition")
@RequiredArgsConstructor
@Tag(name = "메뉴 영양성분", description = "영양성분 등록,조회,수정이 가능합니다")
public class NutritionController {

    private final AuthenticationUtil authenticationUtil;
    private final NutritionService nutritionService;

    @GetMapping("/{menu_id}")
    @Operation(summary = "영양성분 조회", description = "메뉴 ID로 영양성분을 조회합니다")
    @ApiErrorCodeExamples({ErrorCode.MENU_NOT_FOUND, ErrorCode.MENU_STORE_NOT_MATCH})
    public ResponseEntity<CommonResponse<List<NutritionResponseDto>>> getNutritionInfo(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @PathVariable("menu_id") Integer menuId) {

        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        return CommonResponse.ok(nutritionService.getNutritionInfo(storeId, menuId));
    }

    @PostMapping("/{menu_id}")
    @Operation(summary = "영양성분 등록", description = "메뉴 ID의 영양성분을 새로 등록합니다")
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND,ErrorCode.MENU_NOT_FOUND, ErrorCode.MENU_STORE_NOT_MATCH, ErrorCode.NUTRITION_TEMPLATE_NOT_FOUND})
    public ResponseEntity<CommonResponse<Void>> nutritionAdd(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @PathVariable("menu_id") Integer menuId,
            @RequestBody NutritionValuePostRequestDto postRequestDto) {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        nutritionService.nutritionInfoAdd(storeId, menuId, postRequestDto);
        return CommonResponse.ok();
    }

}
