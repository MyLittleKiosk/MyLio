package com.ssafy.mylio.global.error.handler;

import com.ssafy.mylio.global.common.response.CommonResponse;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.ConstraintViolationException;
import lombok.extern.slf4j.Slf4j;
import org.apache.tomcat.util.http.fileupload.impl.SizeLimitExceededException;
import org.springframework.http.ResponseEntity;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.authorization.AuthorizationDeniedException;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import org.springframework.web.multipart.MaxUploadSizeExceededException;
import org.springframework.web.servlet.resource.NoResourceFoundException;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * 비즈니스 로직에서 명시적으로 발생시킨 커스텀 예외 처리
     * 사용법: throw new CustomException(ErrorCode.XXX)
     * 또는: throw new CustomException(ErrorCode.XXX, "paramName", paramValue)
     */
    @ExceptionHandler(CustomException.class)
    protected ResponseEntity<CommonResponse<Object>> handleCustomException(CustomException e, HttpServletRequest request) {
        if (!e.getParameters().isEmpty()) {
            log.error("[CustomException] {} {}: {} - Parameters: {}",
                    request.getMethod(),
                    request.getRequestURI(),
                    e.getMessage(),
                    e.getParameters()
            );
            return CommonResponse.error(e.getErrorCode(), e.getParameters());
        } else {
            log.error("[CustomException] {} {}: {}",
                    request.getMethod(),
                    request.getRequestURI(),
                    e.getMessage()
            );
            return CommonResponse.error(e.getErrorCode());
        }
    }

    /**
     * 요청 DTO 객체의 유효성 검증(@Valid) 실패 시 발생하는 예외 처리
     * 발생 조건: @Valid 어노테이션이 지정된 파라미터의 유효성 검증 실패 시
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    protected ResponseEntity<CommonResponse<Object>> handleMethodArgumentNotValidException(
            MethodArgumentNotValidException e, HttpServletRequest request) {

        FieldError fieldError = e.getBindingResult().getFieldError();

        if (fieldError == null) {
            log.error("[ValidationException] {} {}: 유효성 검증 오류가 발생했지만 필드 에러 정보가 없습니다.",
                    request.getMethod(),
                    request.getRequestURI()
            );
            return CommonResponse.error(ErrorCode.INVALID_INPUT_VALUE, "입력값이 유효하지 않습니다.");
        }

        String field = fieldError.getField();
        String defaultMessage = fieldError.getDefaultMessage();
        Object rejectedValue = fieldError.getRejectedValue();

        log.error("[ValidationException] {} {}: field '{}' - {} (입력값: '{}')",
                request.getMethod(),
                request.getRequestURI(),
                field,
                defaultMessage,
                rejectedValue
        );
        return CommonResponse.error(ErrorCode.INVALID_INPUT_VALUE, rejectedValue + " : " + defaultMessage);
    }

    /**
     * 존재하지 않는 API 엔드포인트 요청 시 발생하는 예외 처리
     * 발생 조건: 매핑되지 않은 URL로 요청이 들어올 때
     */
    @ExceptionHandler(NoResourceFoundException.class)
    protected ResponseEntity<CommonResponse<Object>> handleNoResourceFoundException(
            NoResourceFoundException e, HttpServletRequest request) {
        log.warn("[ResourceNotFound] {} {}", request.getMethod(), request.getRequestURI());
        return CommonResponse.error(ErrorCode.RESOURCE_NOT_FOUND);
    }

    /**
     * 잘못된 인자 값으로 인한 예외 처리
     * 발생 조건:
     * 1. 메서드에 부적절한 인자가 전달될 때
     * 2. 비즈니스 로직에서 throw new IllegalArgumentException() 사용 시
     */
    @ExceptionHandler(IllegalArgumentException.class)
    protected ResponseEntity<CommonResponse<Object>> handleIllegalArgumentException(
            IllegalArgumentException e, HttpServletRequest request) {
        // HTTP 메소드 이름 관련 예외는 보안 시도로 간주
        if (e.getMessage() != null && e.getMessage().contains("HTTP method names must be tokens")) {
            log.warn("[InvalidRequest] Malformed HTTP method from IP: {}",
                    request.getRemoteAddr());
            return CommonResponse.error(ErrorCode.INVALID_INPUT_VALUE);
        }

        // 다른 IllegalArgumentException은 기존대로 처리
        log.error("[IllegalArgument] {} {}: {}",
                request.getMethod(),
                request.getRequestURI(),
                e.getMessage());
        return CommonResponse.error(ErrorCode.INVALID_INPUT_VALUE);
    }

    /**
     * 접근 권한이 없는 경우 발생하는 예외 처리
     * 발생 조건: @PreAuthorize 등의 보안 어노테이션으로 접근이 거부될 때
     */
    @ExceptionHandler(AuthorizationDeniedException.class)
    protected ResponseEntity<CommonResponse<Object>> handleAuthorizationDeniedException(
            AuthorizationDeniedException e, HttpServletRequest request) {

        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
//        String userInfo = auth != null ?
//                auth.getPrincipal() instanceof UserPrincipal ?
//                ((UserPrincipal) auth.getPrincipal()).getId() + " - " + auth.getAuthorities()
//                : "No Authentication";
        String userInfo = auth != null ?
                auth.getPrincipal() instanceof UserPrincipal ?
                        ((UserPrincipal) auth.getPrincipal()).getId() + " - " + auth.getAuthorities()
                        : "No Authentication"
                : "No Authentication";

        log.error("[AccessDenied] {} {}: {} - User: {}",
                request.getMethod(),
                request.getRequestURI(),
                e.getMessage(),
                userInfo
        );

        // 익명 사용자인 경우
        if (auth instanceof AnonymousAuthenticationToken) {
            return CommonResponse.error(ErrorCode.UNAUTHORIZED_ACCESS);
        }

        // 인증은 됐지만 권한이 없는 경우
        return CommonResponse.error(ErrorCode.FORBIDDEN_ACCESS);
    }

    /**
     * @ RequestParam, @PathVariable 등의 제약 조건(@Positive, @NotNull 등) 위반 시 발생하는 예외 처리
     * 발생 조건: 단일 파라미터(@RequestParam 등) 유효성 검증 실패
     */
    @ExceptionHandler(ConstraintViolationException.class)
    protected ResponseEntity<CommonResponse<Object>> handleConstraintViolationException(
            ConstraintViolationException e, HttpServletRequest request) {

        String errorMessage = e.getConstraintViolations()
                .stream()
                .findFirst()
                .map(violation -> violation.getInvalidValue() + " : " + violation.getMessage())
                .orElse("잘못된 요청입니다.");

        log.error("[ConstraintViolationException] {} {}: {}",
                request.getMethod(),
                request.getRequestURI(),
                errorMessage
        );

        return CommonResponse.error(ErrorCode.INVALID_INPUT_VALUE, errorMessage);
    }

    /**
     * @RequestParam 타입 변환 실패 시 발생하는 예외 처리
     * 발생 조건: 잘못된 타입(문자→숫자 등) 요청이 들어올 때
     */
    @ExceptionHandler(MethodArgumentTypeMismatchException.class)
    protected ResponseEntity<CommonResponse<Object>> handleMethodArgumentTypeMismatchException(
            MethodArgumentTypeMismatchException e, HttpServletRequest request) {

        String errorMessage = String.format(
                "잘못된 요청 파라미터 '%s': '%s' → 필요한 타입: %s",
                e.getPropertyName(),
                e.getValue(),
                e.getRequiredType() != null ? e.getRequiredType().getSimpleName() : "알 수 없음"
        );

        log.error("[TypeMismatchException] {} {}: {}",
                request.getMethod(),
                request.getRequestURI(),
                errorMessage
        );

        return CommonResponse.error(ErrorCode.INVALID_INPUT_VALUE, errorMessage);
    }


    /**
     * 기타 모든 처리되지 않은 예외를 처리하는 폴백 핸들러
     * 발생 조건: 위 핸들러에서 처리되지 않은 모든 예외 발생 시
     */
    @ExceptionHandler(Exception.class)
    protected ResponseEntity<CommonResponse<Object>> handleException(Exception e, HttpServletRequest request) {
        log.error("[UnhandledException] {} {}: {}",
                request.getMethod(),
                request.getRequestURI(),
                e.getMessage(),
                e);
        return CommonResponse.error(ErrorCode.INTERNAL_SERVER_ERROR);
    }


}
