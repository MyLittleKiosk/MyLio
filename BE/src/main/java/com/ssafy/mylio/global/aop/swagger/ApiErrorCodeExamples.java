package com.ssafy.mylio.global.aop.swagger;

import com.ssafy.mylio.global.error.code.ErrorCode;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface ApiErrorCodeExamples {
    ErrorCode[] value();
}
