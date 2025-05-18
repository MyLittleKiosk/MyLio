package com.ssafy.mylio.domain.options.controller;

import com.ssafy.mylio.domain.options.dto.request.OptionRequestDto;
import com.ssafy.mylio.domain.options.dto.request.OptionUpdateRequestDto;
import com.ssafy.mylio.domain.options.dto.response.OptionResponseDto;
import com.ssafy.mylio.domain.options.service.OptionService;
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
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/option")
@RequiredArgsConstructor
@Tag(name = "옵션 관리", description = "옵션 조회, 수정, 삭제 등의 API")
public class OptionController {

    private final AuthenticationUtil authenticationUtil;
    private final OptionService optionService;

    @GetMapping
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND})
    @Operation(summary = "옵션 전체 조회", description = "전체 옵션 리스트를 조회합니다.")
    public ResponseEntity<CommonResponse<CustomPage<OptionResponseDto>>> getOptionList(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestParam(name="keyword", required = false) String keyword,
            @PageableDefault(sort = "createdAt", direction = Sort.Direction.DESC) Pageable pageable) {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        return CommonResponse.ok(optionService.getOptionList(storeId, keyword, pageable));
    }

    @GetMapping("/{option_id}")
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND, ErrorCode.OPTION_NOT_FOUND, ErrorCode.OPTION_STORE_NOT_MATCH})
    @Operation(summary = "옵션 상세 조회", description = "optionId로 특정 옵션을 조회합니다.")
    public ResponseEntity<CommonResponse<OptionResponseDto>> getOptionDetail(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @PathVariable("option_id") Integer optionId) {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        return CommonResponse.ok(optionService.getOptionDetail(storeId, optionId));
    }

    @DeleteMapping("/{option_id}")
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND, ErrorCode.OPTION_NOT_FOUND, ErrorCode.OPTION_STORE_NOT_MATCH})
    @Operation(summary = "옵션 삭제", description = "optionId로 특정 옵션을 삭제합니다.")
    public ResponseEntity<CommonResponse<Void>> deleteOption(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @PathVariable("option_id") Integer optionId) {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        optionService.deleteOption(storeId, optionId);
        return CommonResponse.ok();
    }

    @PostMapping
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND})
    @Operation(summary = "옵션 추가", description = "옵션을 추가합니다 (그룹옵션)")
    public ResponseEntity<CommonResponse<Void>> addOption(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @Valid @RequestBody OptionRequestDto optionRequestDto) {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        optionService.addOption(storeId, optionRequestDto);
        return CommonResponse.ok();
    }

    @PatchMapping("/{option_id}")
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND, ErrorCode.OPTION_NOT_FOUND, ErrorCode.OPTION_STORE_NOT_MATCH})
    @Operation(summary = "옵션 수정", description = "optionId로 옵션을 수정합니다 (그룹옵션)")
    public ResponseEntity<CommonResponse<Void>> updateOption(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @Valid @RequestBody OptionUpdateRequestDto optionUpdateRequestDto,
            @PathVariable("option_id") Integer optionId) {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        optionService.updateOption(storeId, optionId, optionUpdateRequestDto);
        return CommonResponse.ok();
    }
}
