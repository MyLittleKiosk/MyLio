package com.ssafy.mylio.domain.options.entity;

import com.ssafy.mylio.global.common.status.EntityStatus;

public enum OptionDetailStatus implements EntityStatus {
    REGISTERED("REGISTERED", "등록됨"),
    HIDDEN("HIDDEN", "숨김"),
    DELETED("DELETED", "삭제됨");

    private final String code;
    private final String description;

    OptionDetailStatus(String code, String description) {
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
