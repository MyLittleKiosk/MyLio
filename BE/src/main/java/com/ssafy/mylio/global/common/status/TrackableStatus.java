package com.ssafy.mylio.global.common.status;

public enum TrackableStatus implements EntityStatus {
    REGISTERED("REGISTERED", "등록됨"),
    UPDATED("UPDATED", "수정됨"),
    DELETED("DELETED", "삭제됨");

    private final String code;
    private final String description;

    TrackableStatus(String code, String description) {
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