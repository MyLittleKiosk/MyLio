package com.ssafy.mylio.domain.options.controller;

import com.ssafy.mylio.domain.options.dto.response.OptionListResponseDto;
import com.ssafy.mylio.domain.options.dto.response.OptionResponseDto;
import com.ssafy.mylio.domain.options.service.OptionService;
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
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

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
    public ResponseEntity<CommonResponse<OptionListResponseDto>> getOptionList(
            @AuthenticationPrincipal UserPrincipal userPrincipal) {
        Integer storeId = authenticationUtil.getCurrentUserId(userPrincipal);
        return CommonResponse.ok(optionService.getOptionList(storeId));
    }
}
