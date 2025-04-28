package com.ssafy.mylio.domain.menu.entity;

import com.ssafy.mylio.global.common.status.EntityStatus;

public enum MenuStatus implements EntityStatus {
    SELLING("selling", "판매중"),
    SOLD_OUT("sold_out", "품절"),
    HIDDEN("hidden", "숨김"),
    DELETED("deleted", "삭제됨");

    private final String code;
    private final String description;

    MenuStatus(String code, String description) {
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