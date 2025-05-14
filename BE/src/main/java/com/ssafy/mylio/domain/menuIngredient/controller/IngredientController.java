package com.ssafy.mylio.domain.menuIngredient.controller;


import com.ssafy.mylio.domain.menuIngredient.dto.response.IngredientTemplateResponseDto;
import com.ssafy.mylio.domain.menuIngredient.service.IngredientService;
import com.ssafy.mylio.global.aop.swagger.ApiErrorCodeExamples;
import com.ssafy.mylio.global.common.CustomPage;
import com.ssafy.mylio.global.common.response.CommonResponse;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import com.ssafy.mylio.global.util.AuthenticationUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/ingredient")
@RequiredArgsConstructor
@Tag(name = "원재료 템플릿", description = "슈퍼관리자가 원재료를 등록,수정,조회합니다")
class IngredientController {

    private final IngredientService ingredientService;
    private final AuthenticationUtil authenticationUtil;

    @GetMapping
    @Operation(summary = "원재료 조회", description = "원재료 목록을 조회할 수 있습니다")
    @ApiErrorCodeExamples({ErrorCode.FORBIDDEN_ACCESS})
    public ResponseEntity<CommonResponse<CustomPage<IngredientTemplateResponseDto>>> getIngredientList(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestParam(name="keyword", required = false) String keyword,
            @PageableDefault(sort = "createdAt", direction = Sort.Direction.DESC) Pageable pageable) {
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        return CommonResponse.ok(ingredientService.getIngredientList(userType, keyword, pageable));
    }

}