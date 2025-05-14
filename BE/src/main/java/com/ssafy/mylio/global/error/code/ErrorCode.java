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
    FORBIDDEN_AUTH(HttpStatus.FORBIDDEN,"C006","인증되지 않은 사용자입니다."),
    // Auth
    REFRESH_TOKEN_NOT_FOUND(HttpStatus.BAD_REQUEST, "A001", "리프레시 토큰이 존재하지 않습니다"),
    INVALID_REFRESH_TOKEN(HttpStatus.UNAUTHORIZED, "A002", "유효하지 않은 리프레시 토큰입니다"),
    INVALID_ACCESS_TOKEN(HttpStatus.UNAUTHORIZED, "A003", "유효하지 않은 액세스 토큰입니다"),
    INVALID_CREDENTIALS(HttpStatus.UNAUTHORIZED, "A004", "아이디 혹은 비밀번호가 일치하지 않습니다."),
    INVALID_ROLE(HttpStatus.UNAUTHORIZED,"A005","권한이 없는 사용자입니다."),
    EMAIL_ALREADY_EXISTS(HttpStatus.CONFLICT,"A006","중복된 이메일입니다."),
    // Menu
    MENU_NOT_FOUND(HttpStatus.NOT_FOUND, "M001", "존재하지 않는 메뉴입니다"),
    MENU_STORE_NOT_MATCH(HttpStatus.BAD_REQUEST,"M002","매장에 없는 메뉴입니다"),

    //Kiosk
    KIOSK_SESSION_NOT_FOUND(HttpStatus.NOT_FOUND,"K001","존재하지 않는 키오스크 입니다."),
    KIOSK_IN_USE(HttpStatus.CONFLICT,"K002","이미 사용중인 키오스크입니다."),
    ALREADY_EXIST_KIOSK(HttpStatus.CONFLICT,"K003","이미 등록된 키오스크 이름입니다."),
    KIOSK_NOT_FOUND(HttpStatus.NOT_FOUND,"K004","존재하지 않는 키오스크입니다."),

    // Store
    STORE_NOT_FOUND(HttpStatus.NOT_FOUND,"S001","존재하지 않는 매장입니다"),
    STORE_DELETED(HttpStatus.NOT_FOUND,"D001","이미 삭제된 계정입니다."),

    // Option
    OPTION_NOT_FOUND(HttpStatus.NOT_FOUND, "O001", "존재하지 않는 옵션입니다"),
    OPTION_STORE_NOT_MATCH(HttpStatus.BAD_REQUEST,"O002","매장에 없는 옵션입니다"),
    OPTION_DETAIL_NOT_FOUND(HttpStatus.NOT_FOUND, "O003", "존재하지 않는 상세옵션입니다"),
    INVALID_OPTION_STATUS(HttpStatus.BAD_REQUEST,"O004","존재하지 않는 옵션 STATUS 입니다"),
    REQUIRED_OPTION_MISSING(HttpStatus.BAD_REQUEST,"O005","필수옵션이 선택되지 않았습니다"),

    //Account
    ACOUNT_NOT_FOUND(HttpStatus.NOT_FOUND, "U001","존재하지 않는 계정 정보입니다."),

    // Category
    CATEGORY_NOT_FOUND(HttpStatus.NOT_FOUND, "CG001", "존재하지 않는 카테고리입니다"),
    CATEGORY_STORE_NOT_MATCH(HttpStatus.BAD_REQUEST,"CG002","매장에 없는 카테고리입니다"),
    INVALID_CATEGORY_STATUS(HttpStatus.BAD_REQUEST,"CG003","존재하지 않는 카테고리 STATUS 입니다"),

    // Nutrition
    NUTRITION_TEMPLATE_NOT_FOUND(HttpStatus.NOT_FOUND, "N001", "존재하지 않는 영양정보 템플릿입니다"),
    NUTRITION_TEMPLATE_ALREADY_EXISTS(HttpStatus.BAD_REQUEST,"N002","이미 존재하는 영양정보 템플릿입니다"),

    // Ingredient
    INGREDIENT_TEMPLATE_NOT_FOUND(HttpStatus.NOT_FOUND, "I001", "존재하지 않는 원재료 템플릿입니다"),
    INGREDIENT_TEMPLATE_ALREADY_EXISTS(HttpStatus.BAD_REQUEST,"I002","이미 존재하는 원재료 템플릿입니다"),

    // AI
    SCREEN_STATE_NOT_FOUND(HttpStatus.BAD_REQUEST,"AI001","렌더링 할 수 없는 STATE 입니다"),
    CART_IS_EMPTY(HttpStatus.BAD_REQUEST,"AI002","장바구니가 비어있습니다"),
    PAY_NOT_MATCH(HttpStatus.BAD_REQUEST,"AI003","등록되지 않은 결제방법입니다"),
    PAY_NOT_FOUND(HttpStatus.BAD_REQUEST,"AI004","결제수단이 정해지지 않았습니다"),

    // Kakao PAY
    PAY_CANCEL(HttpStatus.BAD_REQUEST,"KP001","결제가 취소되었습니다"),
    PAY_FAIL(HttpStatus.INTERNAL_SERVER_ERROR,"KP002","결제를 실패했습니다");

    private final HttpStatus status;
    private final String code;
    private final String message;

}
