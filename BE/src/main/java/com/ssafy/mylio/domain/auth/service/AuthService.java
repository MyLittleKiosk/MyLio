package com.ssafy.mylio.domain.auth.service;

import com.ssafy.mylio.domain.account.entity.Account;
import com.ssafy.mylio.domain.account.entity.AccountRole;
import com.ssafy.mylio.domain.account.repository.AccountRepository;
import com.ssafy.mylio.domain.auth.dto.LoginResult;
import com.ssafy.mylio.domain.auth.dto.request.LoginRequestDto;
import com.ssafy.mylio.domain.auth.dto.response.LoginResponse;
import com.ssafy.mylio.domain.auth.dto.response.StoreInfoResponseDto;
import com.ssafy.mylio.domain.auth.dto.response.SuperInfoResponseDto;
import com.ssafy.mylio.global.common.status.BasicStatus;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import com.ssafy.mylio.global.security.jwt.JwtTokenProvider;
import com.ssafy.mylio.global.security.jwt.TokenValidationResult;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class AuthService {
    private final AccountRepository accountRepository;
    private final JwtTokenProvider jwtTokenProvider;
    private final AuthRedisService authRedisService;


    public LoginResult login(LoginRequestDto request) {
        Account account = accountRepository.findById(request.getId())
                .orElseThrow(() -> new CustomException(ErrorCode.INVALID_CREDENTIALS));

        // 비밀번호 검증예정
        //if(!passwordEncoder.match)
        if (!request.getPassword().equals(account.getPassword())) {
            throw new CustomException(ErrorCode.INVALID_CREDENTIALS);
        }

        //삭제된 user
        if (account.getStatus() == BasicStatus.DELETED) {
            throw new CustomException(ErrorCode.INVALID_CREDENTIALS);

        }
        Integer storeId = (account.getRole() == AccountRole.SUPER)
                ? null
                : account.getStore().getId();
        //JWT 토큰 생성
        String accessToken = jwtTokenProvider.createAccessToken(
                account.getId(),
                storeId,
                account.getRole().getCode()
        );

        String refreshToken = jwtTokenProvider.createRefreshToken(
                account.getId(),
                storeId,
                account.getRole().getCode()
        );

        // Redis에 refreshToken 저장
        authRedisService.saveRefreshToken(account.getId(), refreshToken);

        // 역할별 DTO 응답 분기
        LoginResponse responseDto = (account.getRole() == AccountRole.SUPER)
                ? SuperInfoResponseDto.of(account)
                : StoreInfoResponseDto.of(account);

        return LoginResult.of(responseDto, accessToken, refreshToken);

    }

    public String getRefreshToken(String refreshToken) {
        // 1. Refresh 토큰 유효성 검증
        TokenValidationResult validationResult = jwtTokenProvider.validateToken(refreshToken);
        if (!validationResult.isValid()) {
            throw new CustomException(ErrorCode.INVALID_REFRESH_TOKEN);
        }

        // 2. Redis에 저장된 Refresh 토큰과 비교
        Integer userId = jwtTokenProvider.getUserId(refreshToken);
        Integer storeId = jwtTokenProvider.getStoreId(refreshToken);

        String userType = jwtTokenProvider.getUserType(refreshToken);
        String savedRefreshToken = authRedisService.getRefreshToken(userId);

        if (savedRefreshToken == null || !savedRefreshToken.equals(refreshToken)) {
            throw new CustomException(ErrorCode.INVALID_REFRESH_TOKEN);
        }

        // 3. 새로운 Access 토큰 발급
        return jwtTokenProvider.createAccessToken(userId, storeId, userType);
    }

}
