package com.ssafy.mylio.domain.menu.controller;


import com.ssafy.mylio.domain.menu.dto.request.MenuPostRequestDto;
import com.ssafy.mylio.domain.menu.dto.response.MenuDetailResponseDto;
import com.ssafy.mylio.domain.menu.dto.response.MenuListResponseDto;
import com.ssafy.mylio.domain.menu.service.MenuService;
import com.ssafy.mylio.global.aop.swagger.ApiErrorCodeExample;
import com.ssafy.mylio.global.aop.swagger.ApiErrorCodeExamples;
import com.ssafy.mylio.global.common.CustomPage;
import com.ssafy.mylio.global.common.response.CommonResponse;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import com.ssafy.mylio.global.util.AuthenticationUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.constraints.PositiveOrZero;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.*;

@RestController
@RequiredArgsConstructor
@RequestMapping("/menu")
@Validated
@Tag(name = "메뉴 관리", description = "메뉴 조회, 수정, 삭제 등의 API")
public class MenuController {

    private final MenuService menuService;
    private final AuthenticationUtil authenticationUtil;

    @GetMapping
    @Operation(summary = "메뉴 전체 조회", description = "전체 메뉴 리스트를 조회합니다.")
    public ResponseEntity<CommonResponse<CustomPage<MenuListResponseDto>>> getMenuList(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestParam(name="category_id", required = false) @PositiveOrZero(message = "카테고리 ID는 0 이상 숫자여야 합니다.")  Integer categoryId ,
            @PageableDefault(sort = "createdAt", direction = Sort.Direction.DESC) Pageable pageable){

        Integer storeId = authenticationUtil.getCurrentUserId(userPrincipal);
        return CommonResponse.ok(menuService.getMenuList(storeId, categoryId, pageable));
    }

    @GetMapping("/{menu_id}")
    @Operation(summary = "메뉴 상세 조회", description = "메뉴 정보를 상세조회합니다.")
    @ApiErrorCodeExamples({ErrorCode.MENU_NOT_FOUND})
    public ResponseEntity<CommonResponse<MenuDetailResponseDto>> getMenuDetail(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @PathVariable("menu_id") Integer menuId ) {

        Integer storeId = authenticationUtil.getCurrentUserId(userPrincipal);
        return CommonResponse.ok(menuService.getMenuDetail(storeId, menuId));
    }

    @DeleteMapping("/{menu_id}")
    @Operation(summary = "메뉴 삭제", description = "메뉴를 삭제합니다")
    @ApiErrorCodeExamples({ErrorCode.MENU_NOT_FOUND})
    public ResponseEntity<CommonResponse<Void>> deleteMenu(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @PathVariable("menu_id") Integer menuId) {

        Integer storeId = authenticationUtil.getCurrentUserId(userPrincipal);
        menuService.deleteMenu(storeId, menuId);
        return CommonResponse.ok();
    }

    @PostMapping
    @Operation(summary = "메뉴 등록", description = "새로운 메뉴를 등록합니다")
    @ApiErrorCodeExamples({})
    public ResponseEntity<CommonResponse<Void>> addMenu(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestBody MenuPostRequestDto menuPostRequestDto) {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        menuService.addMenu(storeId, menuPostRequestDto);
        return CommonResponse.ok();
    }
}
