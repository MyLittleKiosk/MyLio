package com.ssafy.mylio.domain.order.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.ssafy.mylio.domain.order.dto.request.OrderRequestDto;
import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import com.ssafy.mylio.domain.order.service.*;
import com.ssafy.mylio.global.common.response.CommonResponse;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import com.ssafy.mylio.global.util.AuthenticationUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.Duration;

@RestController
@RequiredArgsConstructor
@RequestMapping("/order")
@Slf4j
@Tag(name = "음성인식 키오스크", description = "음성인식으로 주문부터 결제까지 진행합니다")
public class GatewayController {

    private final AuthenticationUtil authenticationUtil;
    private final ProxyService proxyService;

    @PostMapping
    @Operation(summary = "음성인식", description = "주문부터 결제까지 진행하는 단일 API")
    public Mono<ResponseEntity<CommonResponse<OrderResponseDto>>> proxy(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @RequestBody OrderRequestDto req) {

        Integer storeId = authenticationUtil.getCurrntStoreId(userPrincipal);
        String role = authenticationUtil.getCurrntUserType(userPrincipal);

        return proxyService.process(storeId, role, userPrincipal, req).map(CommonResponse::ok);
    }
}


