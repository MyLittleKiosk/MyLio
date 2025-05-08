package com.ssafy.mylio.domain.order.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.ssafy.mylio.domain.order.dto.request.OrderRequestDto;
import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import com.ssafy.mylio.domain.order.service.*;
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
    public Mono<ResponseEntity<OrderResponseDto>> proxy(
            @AuthenticationPrincipal UserPrincipal user,
            @RequestBody OrderRequestDto req) {

        Integer storeId = authenticationUtil.getCurrentUserId(user);

        return proxyService.process(storeId, req)
                .map(ResponseEntity::ok);
    }

//    @PostMapping
//    public Mono<ResponseEntity<OrderResponseDto>> proxy(
//            @AuthenticationPrincipal UserPrincipal userPrincipal,
//            @RequestBody OrderRequestDto req) throws JsonProcessingException {
//
//
//        Integer storeId = authenticationUtil.getCurrentUserId(userPrincipal);
//        log.info("storeId : {}", storeId);
//
//        ObjectMapper mapper = new ObjectMapper();
//        mapper.setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE);
//
//        log.info("req 출력 : {}", mapper.writeValueAsString(req));
//
//        // FastAPI 호출
//        Mono<String> fastApiJson = ragWebClient.post()
//                .uri("/recognize_intent")
//                .header("X-DEV-USER", storeId.toString())
//                .contentType(MediaType.APPLICATION_JSON)
//                .bodyValue(mapper.writeValueAsString(req))  // snake_case JSON 그대로 전송
//                .retrieve()
//                .bodyToMono(String.class)            // ← OrderResponseDto 아님!
//                .timeout(Duration.ofSeconds(3));
//
//
//        // 단계별 검증 & 비즈니스 로직 호출
//        return fastApiJson
//                .flatMap(orderValidator::validate)   // validate(String) → Mono<OrderResponseDto>
//                .flatMap(this::dispatchByStatus)     // status 별 비즈니스 처리
//                .map(ResponseEntity::ok);
//
//
////        return ragWebClient.post()
////                .uri("/rag/chat")
////                .header("X-DEV-USER", "1")            // ★ 개발용 인증 헤더
////                .bodyValue(req)           // JSON 직렬화
////                .retrieve()
////                .bodyToMono(OrderResponseDto.class)
////                .timeout(Duration.ofSeconds(3))
////                // ↓↓↓ 검증 로직이 있다면 여기 .doOnNext(validator::validate)
////                .map(ResponseEntity::ok);
//    }

}


