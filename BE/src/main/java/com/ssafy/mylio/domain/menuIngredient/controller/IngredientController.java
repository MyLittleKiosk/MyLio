package com.ssafy.mylio.domain.menuIngredient.controller;


import com.ssafy.mylio.domain.menuIngredient.dto.request.IngredientTemplateRequestDto;
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
import org.springframework.web.bind.annotation.*;

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

    @PostMapping
    @Operation(summary = "원재료 등록", description = "원재료를 등록할 수 있습니다")
    @ApiErrorCodeExamples({ErrorCode.FORBIDDEN_ACCESS, ErrorCode.INGREDIENT_TEMPLATE_ALREADY_EXISTS})
    public ResponseEntity<CommonResponse<Void>> ingredientTemplateAdd(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestBody IngredientTemplateRequestDto requestDto) {
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        ingredientService.ingredientTemplateAdd(userType, requestDto);
        return CommonResponse.ok();
    }

    @PatchMapping("/{ingredient_id}")
    @Operation(summary = "원재료 수정", description = "원재료를 수정할 수 있습니다")
    @ApiErrorCodeExamples({ErrorCode.INGREDIENT_TEMPLATE_NOT_FOUND})
    public ResponseEntity<CommonResponse<Void>> ingredientTemplateUpdate(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @PathVariable("ingredient_id") Integer ingredientId,
            @RequestBody IngredientTemplateRequestDto requestDto) {
        String userType = authenticationUtil.getCurrntUserType(userPrincipal);
        ingredientService.ingredientTemplateUpdate(userType, ingredientId, requestDto);
        return CommonResponse.ok();
    }

}