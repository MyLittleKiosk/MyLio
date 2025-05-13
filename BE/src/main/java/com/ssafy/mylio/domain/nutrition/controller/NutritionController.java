package com.ssafy.mylio.domain.nutrition.controller;

import com.ssafy.mylio.domain.nutrition.service.NutritionService;
import com.ssafy.mylio.global.aop.swagger.ApiErrorCodeExamples;
import com.ssafy.mylio.global.common.response.CommonResponse;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import com.ssafy.mylio.global.util.AuthenticationUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/nutrition")
@RequiredArgsConstructor
@Tag(name = "메뉴 영양성분", description = "영양성분 등록,조회,수정이 가능합니다")
public class NutritionController {

    private final AuthenticationUtil authenticationUtil;
    private final NutritionService nutritionService;

    @GetMapping("/{menu_id}")
    @Operation(summary = "영양성분을 조회합니다", description = "메뉴 ID로 영양성분을 조회합니다")
    @ApiErrorCodeExamples({})
    public ResponseEntity<CommonResponse<Void>> getNutritionInfo(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @PathVariable("menu_id") Integer menuId) {

        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        nutritionService.getNutritionInfo(storeId, menuId);
        return CommonResponse.ok();
    }

}
