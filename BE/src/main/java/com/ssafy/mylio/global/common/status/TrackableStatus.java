package com.ssafy.mylio.global.common.status;

public enum TrackableStatus implements EntityStatus {
    REGISTERED("registered", "등록됨"),
    UPDATED("updated", "수정됨"),
    DELETED("deleted", "삭제됨");

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