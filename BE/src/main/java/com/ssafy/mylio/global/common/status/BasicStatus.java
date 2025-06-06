package com.ssafy.mylio.global.common.status;

public enum BasicStatus implements EntityStatus {
    REGISTERED("REGISTERED", "등록됨"),
    DELETED("DELETED", "삭제됨");

    private final String code;
    private final String description;

    BasicStatus(String code, String description) {
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