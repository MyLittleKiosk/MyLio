package com.ssafy.mylio.domain.options.controller;

import com.ssafy.mylio.domain.options.service.OptionDetailService;
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
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/option_detail")
@RequiredArgsConstructor
@Tag(name = "옵션 상세 관리", description = "옵션 상세수정, 상세삭제 API")
public class OptionDetailController {

    private final OptionDetailService optionDetailService;
    private final AuthenticationUtil authenticationUtil;

    @DeleteMapping("/{option_detail_id}")
    @ApiErrorCodeExamples({ErrorCode.STORE_NOT_FOUND, ErrorCode.OPTION_STORE_NOT_MATCH, ErrorCode.OPTION_DETAIL_NOT_FOUND})
    @Operation(summary = "옵션 상세 삭제", description = "상세 옵션을 삭제합니다.")
    public ResponseEntity<CommonResponse<Void>> deleteOptionDetail(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @PathVariable("option_detail_id") Integer optionDetailId) {
        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        optionDetailService.deleteOptionDetail(storeId, optionDetailId);
        return CommonResponse.ok();
    }
}
