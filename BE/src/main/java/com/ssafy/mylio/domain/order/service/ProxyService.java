package com.ssafy.mylio.domain.order.service;

import com.fasterxml.jackson.core.JsonProcessingException;
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

import java.time.Duration;

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

    private final ObjectMapper snakeMapper = new ObjectMapper()
            .setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE);

    public Mono<OrderResponseDto> process(Integer storeId, OrderRequestDto req) {

        // 1) FastAPI 호출 (String JSON 수신)
        Mono<String> fastApiJson = ragWebClient.post()
                .uri("/recognize_intent")
                .header("X-DEV-USER", storeId.toString())
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(toSnakeJson(req))
                .retrieve()
                .bodyToMono(String.class)
                .timeout(Duration.ofSeconds(3));

        // 2) 검증·교정 → status 분기
        return fastApiJson
                .flatMap(orderValidator::validate)   // String → OrderResponseDto
                .flatMap(this::dispatchByStatus);
    }

    /** camelCase DTO → snake_case JSON */
    private String toSnakeJson(Object dto) {
        try { return snakeMapper.writeValueAsString(dto); }
        catch (JsonProcessingException e) {
            throw new CustomException(ErrorCode.INTERNAL_SERVER_ERROR, "request", "OrderRequestDto");
        }
    }

    /** status 스위칭 */
    private Mono<OrderResponseDto> dispatchByStatus(OrderResponseDto resp) {
        return switch (resp.getScreen_state()) {
            case "ORDER"   -> orderService.handleOrder(resp);

            case "SEARCH"  -> searchValidator.validate(resp).thenReturn(resp);

            case "CONFIRM", "SELECT_PAY", "PAY", "DETAIL"
                    -> paymentValidator.validate(resp)
                    .then(orderService.handlePayment(resp));

            default       -> Mono.error(new IllegalStateException("Unknown status: " + resp.getScreen_state()));
        };
    }
}
