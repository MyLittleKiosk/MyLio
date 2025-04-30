package com.ssafy.mylio.global.error.exception;

import com.ssafy.mylio.global.error.code.ErrorCode;
import lombok.Getter;

import java.util.HashMap;
import java.util.Map;

@Getter
public class CustomException extends RuntimeException {
    private final ErrorCode errorCode;
    private final Map<String, Object> parameters;

    public CustomException (ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
        this.parameters = new HashMap<>();
    }

    public CustomException(ErrorCode errorCode, String message) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
        this.parameters = new HashMap<>();
        this.parameters.put("message", message);
    }

    public CustomException(ErrorCode errorCode, String paramName, Object paramValue) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
        this.parameters = new HashMap<>();
        this.parameters.put(paramName, paramValue);
    }

    public CustomException addParameter(String paramName, Object paramValue) {
        this.parameters.put(paramName, paramValue);
        return this;
    }
}
