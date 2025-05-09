package com.ssafy.mylio.domain.order.service;

import com.ssafy.mylio.domain.order.util.OrderJsonMapper;
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
    private final OrderValidator orderValidator;
    private final SearchValidator searchValidator;
    private final PaymentValidator paymentValidator;
    private final OrderService orderService;
    private final DetailValidator detailValidator;
    private final OrderJsonMapper mapper;

    private final ObjectMapper snakeMapper = new ObjectMapper()
            .setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE);

    public Mono<OrderResponseDto> process(Integer storeId, String role, OrderRequestDto req) {

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
                //.header("X-DEV-USER", storeId.toString())
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(toSnakeJson(req))
                .retrieve()
                .bodyToMono(String.class)
                .timeout(Duration.ofSeconds(5));

        log.info("reg : {}", toSnakeJson(req));

        // 2) 검증·교정 → status 분기
        return fastApiJson
                .flatMap(this::routeByScreenState)  // JSON → OrderResponseDto 및 검증 로직
                .flatMap(this::dispatchByStatus);   // 최종 비즈니스 핸들링
    }

    /** DTO 변환 및 검증 분기처리 */
    private Mono<OrderResponseDto> routeByScreenState(String json) {
        String screen = extractScreenState(json);
        return switch (screen) {
            case "ORDER", "MAIN"  -> orderValidator.validate(json);   // 옵션 검증 포함
            case "DETAIL" -> detailValidator.validate(json);   // 영양정보 검증 포함
            case "SEARCH" -> searchValidator.validate(json);
            case "CONFIRM", "SELECT_PAY" -> paymentValidator.validate(json);
            default -> Mono.fromCallable(() -> mapper.parse(json))
                    .subscribeOn(Schedulers.boundedElastic());
        };
    }

    /** status 스위칭 */
    private Mono<OrderResponseDto> dispatchByStatus(OrderResponseDto resp) {
        return switch (resp.getScreenState()) {
            case "ORDER", "MAIN"   -> orderService.handleOrder(resp);
            case "CONFIRM", "SELECT_PAY", "PAY" -> orderService.handlePayment(resp);
            case "DETAIL", "SEARCH" -> Mono.just(resp);
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
