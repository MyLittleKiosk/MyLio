package com.ssafy.mylio.global.util;

import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class AuthenticationUtil {

    public Integer getCurrentUserId(UserPrincipal userPrincipal) {
        if (userPrincipal == null || userPrincipal.getUserId() == null) {
            throw new CustomException(ErrorCode.UNAUTHORIZED_ACCESS);
        }

        return userPrincipal.getUserId();
    }

    public Integer getCurrntStoreId(UserPrincipal userPrincipal) {
        if (userPrincipal == null || userPrincipal.getStoreId() == null) {
            throw new CustomException(ErrorCode.UNAUTHORIZED_ACCESS);
        }

        return userPrincipal.getStoreId();
    }

    public String getCurrntUserType(UserPrincipal userPrincipal) {
        if (userPrincipal == null || userPrincipal.getUserType() == null) {
            throw new CustomException(ErrorCode.UNAUTHORIZED_ACCESS);
        }

        return userPrincipal.getUserType();
    }
}

