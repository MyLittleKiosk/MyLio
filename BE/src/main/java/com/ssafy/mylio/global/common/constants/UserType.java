package com.ssafy.mylio.global.common.constants;

public enum UserType {
    SUPER,STORE,KIOSK;

    public String getLowerCaseName() {
        return this.name().toLowerCase();
    }

}
