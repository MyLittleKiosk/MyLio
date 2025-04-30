package com.ssafy.mylio.domain.auth.service;

import com.ssafy.mylio.domain.account.entity.Account;
import com.ssafy.mylio.domain.account.entity.AccountRole;
import com.ssafy.mylio.domain.account.repository.AccountRepository;
import com.ssafy.mylio.domain.auth.dto.LoginResult;
import com.ssafy.mylio.domain.auth.dto.request.AdminLoginRequestDto;
import com.ssafy.mylio.domain.auth.dto.request.KioskLoginRequest;
import com.ssafy.mylio.domain.auth.dto.request.LogoutRequest;
import com.ssafy.mylio.domain.auth.dto.response.KioskLoginResponseDto;
import com.ssafy.mylio.domain.auth.dto.response.LoginResponse;
import com.ssafy.mylio.domain.auth.dto.response.StoreInfoResponseDto;
import com.ssafy.mylio.domain.auth.dto.response.SuperInfoResponseDto;
import com.ssafy.mylio.domain.kiosk.entity.KioskSession;
import com.ssafy.mylio.domain.kiosk.repository.KioskRepository;
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
    private final KioskRepository kioskRepository;


    public LoginResult login(AdminLoginRequestDto request) {
        Account account = accountRepository.findById(request.getId())
                .orElseThrow(() -> new CustomException(ErrorCode.INVALID_CREDENTIALS));

        // 비밀번호 검증예정
        //if(!passwordEncoder.match)
        if (!request.getPassword().equals(account.getPassword())) {
            throw new CustomException(ErrorCode.INVALID_CREDENTIALS)
                    .addParameter("accountId",request.getId());
        }

        //삭제된 user
        if (account.getStatus() == BasicStatus.DELETED) {
            throw new CustomException(ErrorCode.INVALID_CREDENTIALS)
                    .addParameter("accountId",request.getId())
                    .addParameter("userType",account.getStatus().getCode());

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

    @Transactional
    public LoginResult kioskLogin(KioskLoginRequest request){
        Account account = accountRepository.findWithStoreById(request.getId())
                .orElseThrow(() -> new CustomException(ErrorCode.INVALID_CREDENTIALS));

        //Store 계정만 접근 가능
        if (account.getRole() != AccountRole.STORE) {
            throw new CustomException(ErrorCode.INVALID_ROLE)
                    .addParameter("role",account.getRole().getCode());
        }

        // null 체크 추가
        if (account.getStore() == null) {
            throw new CustomException(ErrorCode.STORE_NOT_FOUND);
        }

        if (account.getStatus() == BasicStatus.DELETED) {

            throw new CustomException(ErrorCode.INVALID_CREDENTIALS)
                    .addParameter("accountStatus",account.getStatus().getCode());
        }

        if (!request.getPassword().equals(account.getPassword())) {
            log.debug("비밀번호 불일치");
            throw new CustomException(ErrorCode.INVALID_CREDENTIALS);
        }

        Integer storeId = account.getStore().getId();

        //키오스크 조회
        KioskSession session = kioskRepository
                .findByStoreIdAndId(storeId, request.getKioskId())
                .orElseThrow(() -> new CustomException(ErrorCode.KIOSK_SESSION_NOT_FOUND)
                        .addParameter("StoreId",storeId)
                        .addParameter("kioskId",request.getKioskId()));



        //키오스크 상태 확인
        if(session.getIsActive()){
            throw new CustomException(ErrorCode.KIOSK_IN_USE)
                    .addParameter("sessionStatus",session.getIsActive());
        }

        session.updateActive(true);
        kioskRepository.save(session);

        String accessToken = jwtTokenProvider.createAccessToken(
                account.getId(), storeId, AccountRole.KIOSK.getCode());

        String refreshToken = jwtTokenProvider.createRefreshToken(
                account.getId(), storeId, AccountRole.KIOSK.getCode());

        authRedisService.saveRefreshToken(account.getId(), refreshToken);

        LoginResponse response = KioskLoginResponseDto.of(account, session, AccountRole.KIOSK);

        return LoginResult.of(response, accessToken, refreshToken);
    }

    @Transactional
    public void logout(Integer userId, String userType, LogoutRequest request) {
        //토큰 삭제
        authRedisService.deleteRefreshToken(userId);

        //Super , admin인 경우 추작업 없이 끝
        if (!userType.equals(AccountRole.KIOSK.getCode())) {
            return;
        }

        if(request == null){
            log.debug("kioskId is null");
            throw new CustomException(ErrorCode.INVALID_INPUT_VALUE);
        }
        //Kiosk인 경우 상태 false로 변경
        Integer kioskId = request.getKioskId();
        if (kioskId == null) {
            log.debug("kioskId is null");
            throw new CustomException(ErrorCode.KIOSK_SESSION_NOT_FOUND);
        }
        KioskSession session = kioskRepository.findById(kioskId)
                .orElseThrow(() -> new CustomException(ErrorCode.KIOSK_SESSION_NOT_FOUND));

        session.updateActive(false);
        kioskRepository.save(session);

    }

}
