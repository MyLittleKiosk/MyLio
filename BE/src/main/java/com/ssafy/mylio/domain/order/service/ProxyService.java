package com.ssafy.mylio.domain.order.service;

import com.fasterxml.jackson.databind.node.ArrayNode;
import com.ssafy.mylio.domain.order.dto.response.ContentsResponseDto;
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
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

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

    private final ObjectMapper snakeMapper = new ObjectMapper()
            .setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE);

    public Mono<OrderResponseDto> process(Integer storeId, OrderRequestDto req) {

        // 1) FastAPI 호출 (String JSON 수신)
        Mono<String> fastApiJson = ragWebClient.post()
                .uri("/recognize-intent")
                .header("X-DEV-USER", storeId.toString())
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(toSnakeJson(req))
                .retrieve()
                .bodyToMono(String.class)
                .timeout(Duration.ofSeconds(5));

        log.info("reg : {}", toSnakeJson(req));

        // 2) 검증·교정 → status 분기
        return fastApiJson
                .flatMap(this::routeByScreenState)  // JSON → OrderResponseDto 및 검증
                .flatMap(this::dispatchByStatus);   // 최종 비즈니스 핸들링
    }

    // ORDER, DETAIL에 따른 검증 분기 처리
    private Mono<OrderResponseDto> routeByScreenState(String json) {
        String screen = extractScreenState(json);
        return switch (screen) {
            case "ORDER", "MAIN"  -> orderValidator.validate(json);   // 옵션 검증 포함
            case "DETAIL" -> detailValidator.validate(json);   // 영양정보 검증 포함
            default -> Mono.fromCallable(() -> parseOnly(json))
                    .subscribeOn(Schedulers.boundedElastic());
        };
    }

    /** status 스위칭 */
    private Mono<OrderResponseDto> dispatchByStatus(OrderResponseDto resp) {
        return switch (resp.getScreen_state()) {
            case "ORDER"   -> orderService.handleOrder(resp);
            case "SEARCH"  -> searchValidator.validate(resp).thenReturn(resp);
            case "CONFIRM", "SELECT_PAY", "PAY" -> paymentValidator.validate(resp)
                    .then(orderService.handlePayment(resp));
            case "DETAIL", "MAIN" -> Mono.just(resp);
            default -> Mono.error(new IllegalStateException("Unknown status: " + resp.getScreen_state()));
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

    private OrderResponseDto parseOnly(String json) {
        try {
            JsonNode root = snakeMapper.readTree(json);
            JsonNode data = root.path("data");

            // root 노드 값 파싱
            String status  = root.path("screen_state").asText(null);
            String payment = root.path("payment_method").isNull() ? null : root.path("payment_method").asText();

            // data 값 파싱
            String preText = data.path("pre_text").asText(null);
            String postText = data.path("post_text").asText(null);
            String reply = data.path("reply").asText(null);
            String sessionId = data.path("session_id").asText(null);

            // 필요하다면 contents 배열 길이만 파악
            List<ContentsResponseDto> contents = Collections.emptyList();
            if (root.path("data").has("contents")) {
                contents = new ArrayList<>();
                for (JsonNode m : (ArrayNode) root.path("data").path("contents")) {
                    contents.add(
                            ContentsResponseDto.builder()
                                    .menuId(m.path("menu_id").asInt())
                                    .quantity(m.path("quantity").asInt())
                                    .name(m.path("name").asText(null))
                                    .build()
                    );
                }
            }

            return OrderResponseDto.builder()
                    .preText(preText)
                    .postText(postText)
                    .reply(reply)
                    .screen_state(status)
                    .language("KR")
                    .sessionId(sessionId)
                    .payment(payment)
                    .cart(Collections.emptyList())
                    .contents(contents)
                    .build();
        } catch (IOException e) {
            throw new CustomException(ErrorCode.INTERNAL_SERVER_ERROR, "payload", "order-json");
        }
    }
}
