package com.ssafy.mylio.domain.payment.entity;

import com.ssafy.mylio.global.common.status.EntityStatus;

public enum PaymentMethod implements EntityStatus {
    CARD("card", "카드"),
    CASH("cash", "현금"),
    MOBILE("mobile", "모바일결제"),
    POINTS("points", "포인트");

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
}