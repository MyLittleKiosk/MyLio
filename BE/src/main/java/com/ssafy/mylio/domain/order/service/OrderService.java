package com.ssafy.mylio.domain.order.service;

import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import com.ssafy.mylio.domain.order.repository.OrderRepository;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepo;

    /* 옵션 검증 완료 → 장바구니 업데이트 등 */
    public Mono<OrderResponseDto> handleOrder(OrderResponseDto resp, UserPrincipal user) {
        // 예: totalPrice 재계산, cart 에 push
        return Mono.just(resp);
    }

    /* CONFIRM → SELECT_PAY → PAY 단계 */
    public Mono<OrderResponseDto> handlePayment(OrderResponseDto resp, UserPrincipal user) {
        if (resp.getScreenState().equals("PAY")) {
            //orderRepo.saveAll(OrderEntity.of(resp.getCart())); // DB 저장
        }
        return Mono.just(resp);
    }
}
