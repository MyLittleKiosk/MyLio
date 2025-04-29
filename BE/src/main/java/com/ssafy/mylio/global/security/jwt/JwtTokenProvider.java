package com.ssafy.mylio.global.security.jwt;

import com.ssafy.mylio.global.common.constants.SecurityConstants;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.stereotype.Component;
import static io.jsonwebtoken.Jwts.SIG; // ⚠️ 이 import 중요!


import javax.crypto.SecretKey;
import java.util.Collections;
import java.util.Date;

@Component
@RequiredArgsConstructor
public class JwtTokenProvider {

    @Value("${jwt.secret}")
    private String secretKey;

    // SecretKey 생성
    private SecretKey getSigningKey() {
        byte[] keyBytes = Decoders.BASE64.decode(secretKey);
        return Keys.hmacShaKeyFor(keyBytes);
    }

    // 기존 토큰 생성 메소드 유지
    public String createToken(Integer userId,Integer storeId, String userType, long validityTime) {
        Date now = new Date();

        return Jwts.builder()
                .subject(Integer.toString(userId))
                .claim(SecurityConstants.ROLE_NAME, userType)
                .claim("storeId", storeId)
                .issuedAt(now)
                .expiration(new Date(now.getTime() + validityTime))
                .signWith(getSigningKey(), SIG.HS256)  // 추천 방식
                .compact();
    }

    // Refresh Token 생성
    public String createAccessToken(Integer userId,Integer storeId, String userType) {
        long accessTokenValidTime = SecurityConstants.ACCESS_TOKEN_VALIDITY_SECONDS * 1000L;
        return createToken(userId, storeId,userType, accessTokenValidTime);
    }

    // Refresh Token 생성
    public String createRefreshToken(Integer userId,Integer storeId, String userType) {
        long refreshTokenValidTime = SecurityConstants.REFRESH_TOKEN_VALIDITY_SECONDS * 1000L;
        return createToken(userId, storeId,userType, refreshTokenValidTime);
    }

    // 토큰에서 회원 정보 추출
    public Integer getUserId(String token) {
        return Integer.parseInt(extractAllClaims(token).getSubject());
    }

    // 토큰에서 storeId 정보 추출
    public Integer getStoreId(String token) {
        Integer storeId= extractAllClaims(token).get("storeId", Integer.class);
        if (storeId == null) {
            return null; // 또는 Optional.empty() 처리도 가능
        }
        return storeId;
    }

    public String getUserType(String token) {
        return extractAllClaims(token).get(SecurityConstants.ROLE_NAME, String.class);
    }

    // Claims 추출
    private Claims extractAllClaims(String token) {
        return Jwts.parser()
                .verifyWith(getSigningKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }

    // 토큰 유효성 + 만료일자 확인
    public TokenValidationResult validateToken(String token) {
        try {
            extractAllClaims(token);
            return new TokenValidationResult(true, null);
        } catch (ExpiredJwtException e) {
            return new TokenValidationResult(false, TokenError.EXPIRED);
        } catch (Exception e) {
            return new TokenValidationResult(false, TokenError.INVALID);
        }
    }

    // Spring Security 인증 객체 생성
    public Authentication getAuthentication(String token) {
        Integer userId = getUserId(token);
        Integer storeId = getStoreId(token);
        String userType = getUserType(token);

        UserPrincipal userPrincipal = UserPrincipal.builder()
                .userId(userId)
                .storeId(storeId)
                .authorities(Collections.singletonList(new SimpleGrantedAuthority(SecurityConstants.ROLE_PREFIX + userType)))
                .build();

        return new UsernamePasswordAuthenticationToken(
                userPrincipal,
                "",
                userPrincipal.getAuthorities());
    }
}
