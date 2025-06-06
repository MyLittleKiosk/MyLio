package com.ssafy.mylio.global.config.security;

import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.security.DevAuthenticationFilter;
import com.ssafy.mylio.global.security.jwt.JwtAuthenticationFilter;
import com.ssafy.mylio.global.security.jwt.JwtTokenProvider;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Arrays;
import java.util.List;

@Slf4j
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    @Value("${app.domain.cors-origins}")
    private List<String> allowedOrigins;

    private final JwtTokenProvider jwtTokenProvider;

    @Autowired(required = false)
    private DevAuthenticationFilter devAuthenticationFilter;

    private final Environment environment;

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public JwtAuthenticationFilter jwtAuthenticationFilter() {
        return new JwtAuthenticationFilter(jwtTokenProvider);
    }


    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                .cors(cors -> cors.configurationSource(corsConfigurationSource()))  // prefilght(OPTIONS) 처리 목적 추가
                .csrf(AbstractHttpConfigurer::disable)
                .sessionManagement(session ->
                        session.sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                )
                // 여기에 exceptionHandling 추가
                .exceptionHandling(exceptions -> exceptions
                        .authenticationEntryPoint((request, response, authException) -> {
                            log.error("인증 오류 (401 Unauthorized): {}", authException.getMessage());

                            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED); // 401
                            response.setContentType("application/json;charset=UTF-8");

                            String errorJson = String.format(
                                    "{\"success\": false, \"data\": null, \"error\": {\"code\": \"%s\", \"message\": \"%s\"}, \"timestamp\": \"%s\"}",
                                    ErrorCode.UNAUTHORIZED_ACCESS.getCode(),
                                    ErrorCode.UNAUTHORIZED_ACCESS.getMessage(),
                                    java.time.LocalDateTime.now()
                            );
                            response.getWriter().write(errorJson);
                        })
                        .accessDeniedHandler((request, response, accessDeniedException) -> {
                            log.error("접근 거부 (403 Forbidden): {}", accessDeniedException.getMessage());

                            response.setStatus(HttpServletResponse.SC_FORBIDDEN); // 403
                            response.setContentType("application/json;charset=UTF-8");

                            String errorJson = String.format(
                                    "{\"success\": false, \"data\": null, \"error\": {\"code\": \"%s\", \"message\": \"%s\"}, \"timestamp\": \"%s\"}",
                                    ErrorCode.FORBIDDEN_ACCESS.getCode(),
                                    ErrorCode.FORBIDDEN_ACCESS.getMessage(),
                                    java.time.LocalDateTime.now()
                            );
                            response.getWriter().write(errorJson);
                        })
                )
                .authorizeHttpRequests(authorize ->
                        authorize
                                .requestMatchers("/auth/login","/auth/login/kiosk","/test",
                                        "/account/pw", "/auth/refresh"  ).permitAll()
                                .requestMatchers("/swagger-ui/**", "/v3/api-docs/**").permitAll()
                                .requestMatchers("/actuator/**").permitAll()
                                .requestMatchers(HttpMethod.POST, "/order").permitAll()  // ★ local
                                .anyRequest().authenticated()
                );

        // 개발 환경 필터는 조건부로 추가
        if (isDevOrLocalProfile() && devAuthenticationFilter != null) {
            log.info("개발 환경 인증 필터를 추가합니다.");
            http.addFilterBefore(devAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);
        }
        http.addFilterBefore(jwtAuthenticationFilter(), UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    private boolean isDevOrLocalProfile() {
        return Arrays.stream(environment.getActiveProfiles())
                .anyMatch(profile -> profile.equals("dev") || profile.equals("local"));
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        log.info("CORS 설정 중... 허용된 오리진: {}", allowedOrigins);
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOrigins(allowedOrigins);
        configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"));
        configuration.setAllowedHeaders(Arrays.asList(
                "Authorization", "Content-Type", "X-Requested-With",
                "Access-Control-Allow-Credentials", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers",
                "Accept", "Origin", "Cookie", "Set-Cookie", "X-DEV-USER",
                "Cache-Control", "Connection"
        ));
        configuration.setExposedHeaders(List.of("Set-Cookie"));  // 쿠키 노출 허용
        configuration.setAllowCredentials(true);
        configuration.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}