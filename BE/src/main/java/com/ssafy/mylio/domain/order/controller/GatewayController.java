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
public class GatewayController {

    private final AuthenticationUtil authenticationUtil;
    private final ProxyService proxyService;

    @PostMapping
    public Mono<ResponseEntity<CommonResponse<OrderResponseDto>>> proxy(
            @AuthenticationPrincipal UserPrincipal user,
            @RequestBody OrderRequestDto req) {

        Integer storeId = authenticationUtil.getCurrentUserId(user);

        return proxyService.process(storeId, req).map(CommonResponse::ok);
    }
}


