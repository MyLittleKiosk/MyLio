package com.ssafy.mylio.domain.auth.service;


import com.ssafy.mylio.global.common.constants.SecurityConstants;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;

@Slf4j
@Service
@RequiredArgsConstructor
public class AuthRedisService {
    private final StringRedisTemplate redisTemplate;

    //RefreshToken 저장
    public void saveRefreshToken(int userId, String refreshToken){
        String key = getRefreshTokenKey(userId);
        redisTemplate.opsForValue().set(
                key,
                refreshToken,
                SecurityConstants.REFRESH_TOKEN_VALIDITY_SECONDS,
                TimeUnit.SECONDS
        );
    }

    //RefreshToken 조회
    public String getRefreshToken(int userId){
        return redisTemplate.opsForValue().get(getRefreshTokenKey(userId));
    }

    public String getRefreshTokenKey(int userId){return "refresh_token"+(Integer.toString(userId));}

    //RefreshToken 삭제
    public void deleteRefreshToken(int userId){redisTemplate.delete(getRefreshTokenKey(userId));}
}
