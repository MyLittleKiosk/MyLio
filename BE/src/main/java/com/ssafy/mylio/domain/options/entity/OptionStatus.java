package com.ssafy.mylio.domain.options.entity;

import com.ssafy.mylio.global.common.status.EntityStatus;

public enum OptionStatus implements EntityStatus {
    REGISTERED("registered", "등록됨"),
    HIDDEN("hidden", "숨김"),
    DELETED("deleted", "삭제됨");

    private final String code;
    private final String description;

    OptionStatus(String code, String description) {
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
