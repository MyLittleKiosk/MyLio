package com.ssafy.mylio.global.security.auth;

import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.security.core.GrantedAuthority;

import java.util.Collection;
import java.util.Map;

@Getter
@NoArgsConstructor
public class UserPrincipal {
    private Integer userId;
    private Integer storeId;
    private String userType;
    private Collection<? extends GrantedAuthority> authorities;
    private Map<String, Object> attributes;

    @Builder
    public UserPrincipal(Integer userId,Integer storeId, Collection<? extends GrantedAuthority> authorities, String userType) {
        this.userId = userId;
        this.storeId = storeId;
        this.authorities = authorities;
        this.userType = userType;
    }
}