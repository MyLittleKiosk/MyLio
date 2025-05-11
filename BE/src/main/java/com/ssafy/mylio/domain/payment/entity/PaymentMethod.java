package com.ssafy.mylio.domain.payment.entity;

import com.ssafy.mylio.global.common.status.EntityStatus;

import java.util.Arrays;

public enum PaymentMethod implements EntityStatus {
    CARD("CARD", "카드"),
    PAY("PAY", "카카오페이"),
    MOBILE("MOBILE", "모바일결제"),
    GIFT("GIFT", "기프트 카드");

    private final String code;
    private final String description;

    PaymentMethod(String code, String description) {
        this.code = code;
        this.description = description;
    }

    @Override
    public String getCode() {
        return code;
    }

    @Override
    public String getDescription() {
        return description;
    }

    public static PaymentMethod fromCode(String code) {
        return Arrays.stream(PaymentMethod.values())
                .filter(p -> p.getCode().equalsIgnoreCase(code))
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException("Unknown payment method code: " + code));
    }

}