package com.ssafy.mylio.domain.payment.entity;

import com.ssafy.mylio.global.common.status.EntityStatus;

public enum PaymentStatus implements EntityStatus {
    READY("READY", "결제 준비"),
    SUCCESS("SUCCESS", "결제 성공"),
    FAIL("FAIL", "결제 실패"),
    CANCEL("CANCEL", "결제 취소");

    private final String code;
    private final String description;

    PaymentStatus(String code, String description) {
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