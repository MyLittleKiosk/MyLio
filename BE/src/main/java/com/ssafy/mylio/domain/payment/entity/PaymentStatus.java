package com.ssafy.mylio.domain.payment.entity;

import com.ssafy.mylio.global.common.status.EntityStatus;

public enum PaymentStatus implements EntityStatus {
    READY("ready", "결제 준비"),
    SUCCESS("success", "결제 성공"),
    FAIL("fail", "결제 실패"),
    CANCEL("cancel", "결제 취소");

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