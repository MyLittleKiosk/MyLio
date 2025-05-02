package com.ssafy.mylio.domain.order.entity;

import com.ssafy.mylio.global.common.status.EntityStatus;

public enum OrderStatus implements EntityStatus {
    DINEIN("DIVE_IN", "매장 식사"),
    TAKEOUT("TAKE_OUT", "포장");

    private final String code;
    private final String description;

    OrderStatus(String code, String description) {
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