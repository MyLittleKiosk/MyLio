package com.ssafy.mylio.domain.account.entity;

public enum AccountRole {
    STORE("STORE","매장"),
    SUPER("SUPER","관리자"),
    KIOSK("KIOSK","키오스크");

    private final String code;
    private final String description;

    AccountRole(String code , String description){
        this.code = code;
        this.description = description;
    }

    public String getCode() {
        return code;
    }

    public String getDescription() {
        return description;
    }
}