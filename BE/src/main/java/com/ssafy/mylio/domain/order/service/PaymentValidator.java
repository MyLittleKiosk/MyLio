package com.ssafy.mylio.domain.order.service;

import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.util.EnumSet;

@Service
public class PaymentValidator {

    public Mono<Void> validate(OrderResponseDto resp) {
        return Mono.fromRunnable(() -> {
            String status = resp.getStatus();
            if (status.equals("CONFIRM") && resp.getCart().isEmpty())
                throw new CustomException(ErrorCode.MENU_NOT_FOUND, "장바구니가 비어 있습니다.");

            if (status.equals("SELECT_PAY"))
                throw new CustomException(ErrorCode.MENU_NOT_FOUND, "장바구니가 비어 있습니다.");
        });
    }
}
