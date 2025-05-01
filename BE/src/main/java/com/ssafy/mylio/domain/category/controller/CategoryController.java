package com.ssafy.mylio.domain.category.controller;

import com.ssafy.mylio.domain.category.dto.request.CategoryAddRequestDto;
import com.ssafy.mylio.domain.category.dto.request.CategoryUpdateRequestDto;
import com.ssafy.mylio.domain.category.dto.response.CategoryResponseDto;
import com.ssafy.mylio.domain.category.service.CategoryService;
import com.ssafy.mylio.global.aop.swagger.ApiErrorCodeExamples;
import com.ssafy.mylio.global.common.CustomPage;
import com.ssafy.mylio.global.common.response.CommonResponse;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import com.ssafy.mylio.global.util.AuthenticationUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
@RequestMapping("/category")
@RequiredArgsConstructor
@Tag(name = "카테고리 관리", description = "카테고리 조회, 등록, 수정, 삭제 API")
public class CategoryController {

    private final AuthenticationUtil authenticationUtil;
    private final CategoryService categoryService;

    @GetMapping
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND})
    @Operation(summary = "카테고리 조회", description = "카테고리 목록을 조회합니다")
    public ResponseEntity<CommonResponse<CustomPage<CategoryResponseDto>>> getCategoryList(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @PageableDefault(sort = "createdAt", direction = Sort.Direction.DESC) Pageable pageable) {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        return CommonResponse.ok(categoryService.getCategoryList(storeId, pageable));
    }

    @PostMapping
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND})
    @Operation(summary = "카테고리 등록", description = "카테고리를 등록합니다")
    public ResponseEntity<CommonResponse<Void>> addCategory(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @Valid @RequestBody CategoryAddRequestDto categoryAddRequestDto) {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        categoryService.addCategory(storeId, categoryAddRequestDto);
        return CommonResponse.ok();
    }

    @PatchMapping("/{category_id}")
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND, ErrorCode.CATEGORY_NOT_FOUND, ErrorCode.CATEGORY_STORE_NOT_MATCH, ErrorCode.INVALID_CATEGORY_STATUS})
    @Operation(summary = "카테고리 수정", description = "category_id로 카테고리를 수정합니다")
    public ResponseEntity<CommonResponse<Void>> updateCategory(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @Valid @RequestBody CategoryUpdateRequestDto categoryUpdateRequestDto,
            @PathVariable("category_id") Integer categoryId) {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        categoryService.updateCategory(storeId, categoryId, categoryUpdateRequestDto);
        return CommonResponse.ok();
    }

    @DeleteMapping("/{category_id}")
    @ApiErrorCodeExamples({})
    @Operation(summary = "카테고리 삭제", description = "category_id로 카테고리를 삭제합니다")
    public ResponseEntity<CommonResponse<Void>> deleteCategory(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @PathVariable("category_id") Integer categoryId) {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        categoryService.deleteCategory(storeId, categoryId);
        return CommonResponse.ok();
    }
}
