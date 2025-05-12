package com.ssafy.mylio.domain.order.service;

import com.ssafy.mylio.domain.order.util.OrderJsonMapper;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import reactor.core.scheduler.Schedulers;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.ssafy.mylio.domain.order.dto.request.OrderRequestDto;
import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import com.ssafy.mylio.global.error.code.ErrorCode;

import java.io.IOException;
import java.time.Duration;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Slf4j
public class ProxyService {

    @Qualifier("ragWebClient")
    private final WebClient ragWebClient;
    private final OrderValidatorService orderValidatorService;
    private final SearchValidatorService searchValidatorService;
    private final PaymentValidatorService paymentValidatorService;
    private final OrderService orderService;
    private final DetailValidatorService detailValidatorService;
    private final OrderJsonMapper mapper;

    private final ObjectMapper snakeMapper = new ObjectMapper()
            .setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE);

    public Mono<OrderResponseDto> process(Integer storeId, String role, UserPrincipal user, OrderRequestDto req) {

        if(!role.equals("KIOSK")){
            throw new CustomException(ErrorCode.FORBIDDEN_ACCESS,"role",role);
        }

        // storeId
        req.setStoreId(storeId);

        // sessionId
        if(req.getSessionId() == null || req.getSessionId().isBlank()){
            req.setSessionId(UUID.randomUUID().toString());
        }

        // 1) FastAPI 호출 (String JSON 수신)
        Mono<String> fastApiJson = ragWebClient.post()
                .uri("/ai/recognize-intent")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(toSnakeJson(req))
                .retrieve()
                .bodyToMono(String.class)
                .timeout(Duration.ofSeconds(10));

        log.info("reg : {}", toSnakeJson(req));

        // 2) 검증·교정 → status 분기
        return fastApiJson
                .flatMap(json -> routeByScreenState(json, user)) // JSON → OrderResponseDto 및 검증 로직
                .flatMap(resp -> dispatchByStatus(resp, user));   // 최종 비즈니스 핸들링

    }

    /** DTO 변환 및 검증 분기처리 */
    private Mono<OrderResponseDto> routeByScreenState(String json, UserPrincipal user) {
        String screen = extractScreenState(json);
        return switch (screen) {
            case "ORDER", "MAIN"  -> orderValidatorService.validate(json, user);   // 옵션 검증 포함
            case "DETAIL" -> detailValidatorService.validate(json, user);   // 영양정보 검증 포함
            case "SEARCH" -> searchValidatorService.validate(json, user);
            case "CONFIRM", "SELECT_PAY" , "PAY"-> paymentValidatorService.validate(json, user);
            default -> Mono.fromCallable(() -> mapper.parse(json, user))
                    .subscribeOn(Schedulers.boundedElastic());
        };
    }

    /** status 스위칭 */
    private Mono<OrderResponseDto> dispatchByStatus(OrderResponseDto resp, UserPrincipal user) {
        return switch (resp.getScreenState()) {
            case "ORDER", "MAIN"   -> orderService.handleOrder(resp,user);
            case "PAY" -> orderService.handlePayment(resp,user);
            case "DETAIL", "SEARCH", "CONFIRM", "SELECT_PAY" -> Mono.just(resp);
            default -> Mono.error(new CustomException(ErrorCode.SCREEN_STATE_NOT_FOUND, "status: " + resp.getScreenState()));
        };
    }

    /** camelCase DTO → snake_case JSON */
    private String toSnakeJson(Object dto) {
        try { return snakeMapper.writeValueAsString(dto); }
        catch (IOException e) {
            throw new CustomException(ErrorCode.INTERNAL_SERVER_ERROR, "request", "OrderRequestDto");
        }
    }

    private String extractScreenState(String json) {
        try {
            JsonNode root = snakeMapper.readTree(json);
            return root.path("screen_state").asText(null);
        } catch (IOException e) {
            throw new CustomException(ErrorCode.INTERNAL_SERVER_ERROR, "payload", "screen_state");
        }
    }
}
