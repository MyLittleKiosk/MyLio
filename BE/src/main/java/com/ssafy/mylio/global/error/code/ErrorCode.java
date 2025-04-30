package com.ssafy.mylio.global.error.code;


import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
@AllArgsConstructor
public enum ErrorCode {

    // Common
    INVALID_INPUT_VALUE(HttpStatus.BAD_REQUEST, "C001", "잘못된 입력값입니다"),
    RESOURCE_NOT_FOUND(HttpStatus.NOT_FOUND, "C002", "요청한 리소스를 찾을 수 없습니다"),
    INTERNAL_SERVER_ERROR(HttpStatus.INTERNAL_SERVER_ERROR, "C003", "서버 내부 오류가 발생했습니다"),
    UNAUTHORIZED_ACCESS(HttpStatus.UNAUTHORIZED, "C004", "로그인이 필요한 서비스입니다"),
    FORBIDDEN_ACCESS(HttpStatus.FORBIDDEN, "C005", "접근 권한이 없습니다"),

    // Auth
    REFRESH_TOKEN_NOT_FOUND(HttpStatus.BAD_REQUEST, "A001", "리프레시 토큰이 존재하지 않습니다"),
    INVALID_REFRESH_TOKEN(HttpStatus.UNAUTHORIZED, "A002", "유효하지 않은 리프레시 토큰입니다"),
    INVALID_ACCESS_TOKEN(HttpStatus.UNAUTHORIZED, "A003", "유효하지 않은 액세스 토큰입니다"),
    INVALID_CREDENTIALS(HttpStatus.UNAUTHORIZED, "A004", "아이디 혹은 비밀번호가 일치하지 않습니다."),
    INVALID_ROLE(HttpStatus.UNAUTHORIZED,"A005","권한이 없는 사용자입니다."),

    // Menu
    MENU_NOT_FOUND(HttpStatus.NOT_FOUND, "M001", "존재하지 않는 메뉴입니다"),

    //Kiosk
    KIOSK_SESSION_NOT_FOUND(HttpStatus.NOT_FOUND,"K001","존재하지 않는 키오스크 입니다."),
    KIOSK_IN_USE(HttpStatus.CONFLICT,"K002","이미 사용중인 키오스크입니다."),

    // Store
    STORE_NOT_FOUND(HttpStatus.NOT_FOUND,"S001","존재하지 않는 매장입니다"),

    // Option
    OPTION_NOT_FOUND(HttpStatus.NOT_FOUND, "O001", "존재하지 않는 옵션입니다"),
    OPTION_STORE_NOT_MATCH(HttpStatus.BAD_REQUEST,"O002","매장에 없는 옵션입니다"),
    OPTION_DETAIL_NOT_FOUND(HttpStatus.NOT_FOUND, "O003", "존재하지 않는 상세옵션입니다"),
    INVALID_OPTION_STATUS(HttpStatus.BAD_REQUEST,"O004","존재하지 않는 옵션 STATUS 입니다"),

    //Account
    ACOUNT_NOT_FOUND(HttpStatus.NOT_FOUND, "U001","존재하지 않는 계정 정보입니다.");

    private final HttpStatus status;
    private final String code;
    private final String message;

}
