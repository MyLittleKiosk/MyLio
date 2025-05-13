package com.ssafy.mylio.domain.payment.service;

import com.ssafy.mylio.domain.order.service.OrderService;
import com.ssafy.mylio.domain.payment.dto.request.KakaoPayApproveRequestDto;
import com.ssafy.mylio.domain.payment.dto.request.PayRequestDto;
import com.ssafy.mylio.domain.payment.dto.response.ApproveResponseDto;
import com.ssafy.mylio.domain.payment.dto.response.ReadyResponseDto;
import com.ssafy.mylio.domain.payment.entity.PaymentMethod;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;


@Service
@RequiredArgsConstructor
@Slf4j
public class KakaoPayService implements PayService {

    @Value("${app.domain.url}")
    private String BASE_URL;

    @Value("${spring.pay.kakao.secret}")
    private String SECRET_KEY;

    @Value("${spring.pay.kakao.ready-url}")
    private String READY_URL;

    @Value("${spring.pay.kakao.approve-url}")
    private String APPROVE_URL;

    private final WebClient webClient;
    private final StringRedisTemplate redisTemplate;
    private static final String REDIS_KEY_PREFIX = "pay:tid:";
    private static final String CID = "TC0ONETIME";

    private final OrderService orderService;

    @Override
    public Mono<ReadyResponseDto> readyToPay(Integer userId, PayRequestDto payRequestDto){
        Map<String, Object> body = new HashMap<>();
        body.put("cid", CID);
        body.put("partner_order_id", payRequestDto.getSessionId());
        body.put("partner_user_id", userId);
        body.put("item_name", payRequestDto.getItemName());
        body.put("quantity", "1");
        body.put("total_amount", payRequestDto.getTotalAmount());
        body.put("tax_free_amount",0);
        body.put("approval_url", BASE_URL +"/api/pay/success-view?orderId=" + payRequestDto.getSessionId());
        body.put("cancel_url", BASE_URL +"/api/pay/cancel");
        body.put("fail_url", BASE_URL + "/api/pay/fail");

        // rest
        return webClient.post()
                .uri(READY_URL)
                .header(HttpHeaders.AUTHORIZATION, "SECRET_KEY " + SECRET_KEY)
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(body)
                .retrieve()
                .onStatus(status -> status.is4xxClientError() || status.is5xxServerError(), response ->
                        response.bodyToMono(String.class).flatMap(errorBody -> {
                            log.error("카카오페이 오류: {}", errorBody);
                            return Mono.error(new RuntimeException("카카오페이 요청 실패: " + errorBody));
                        })
                )
                .bodyToMono(ReadyResponseDto.class)
                .doOnNext(readyResponse -> {
                    redisTemplate.opsForValue().set(
                            REDIS_KEY_PREFIX + payRequestDto.getSessionId(),
                            readyResponse.getTid(),
                            Duration.ofMinutes(10)
                    );
                });

    }

    @Override
    public Mono<ApproveResponseDto> approveToPay(KakaoPayApproveRequestDto dto, Integer userId, Integer storeId){
        // Redis에서 TID 조회
        String tid = redisTemplate.opsForValue().get(REDIS_KEY_PREFIX + dto.getOrderId());

        Map<String, Object> body = new HashMap<>();
        body.put("cid", CID);
        body.put("tid", tid);
        body.put("partner_order_id", dto.getOrderId());
        body.put("partner_user_id", userId);
        body.put("pg_token", dto.getPgToken());

        return webClient.post()
                .uri(APPROVE_URL)
                .header(HttpHeaders.AUTHORIZATION, "SECRET_KEY " + SECRET_KEY)
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(body)
                .retrieve()
                .onStatus(status -> status.is4xxClientError() || status.is5xxServerError(), response ->
                        response.bodyToMono(String.class).flatMap(errorBody -> {
                            log.error("카카오페이 오류: {}", errorBody);
                            return Mono.error(new RuntimeException("카카오페이 요청 실패: " + errorBody));
                        })
                )
                .bodyToMono(ApproveResponseDto.class)
                .flatMap(approveResponse -> {
                    // 3. 결제 승인 성공 → 주문 저장
                    return orderService.saveOrderAfterKakaoPay(storeId, dto.getCart())
                            .thenReturn(approveResponse); // 저장 성공 후 응답 리턴
                });
    }

    @Override
    public PaymentMethod getPaymentMethod() {
        return PaymentMethod.PAY;
    }
}
