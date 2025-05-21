package com.ssafy.mylio.domain.payment.strategy;

import com.ssafy.mylio.domain.payment.entity.PaymentMethod;
import com.ssafy.mylio.global.common.constants.PayType;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

@Component
public class PaymenyFactory {

    private final Map<PaymentMethod, PayStrategy> strategies;


    public PaymenyFactory(List<PayStrategy> strategies) {
        this.strategies = strategies.stream()
                .collect(Collectors.toMap(PayStrategy::getPaymentMethod,
                        Function.identity()));
    }

    public PayStrategy of(PaymentMethod paymentMethod) {
        return strategies.get(paymentMethod);
    }

}
