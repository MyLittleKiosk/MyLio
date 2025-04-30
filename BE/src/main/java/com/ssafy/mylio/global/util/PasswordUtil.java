package com.ssafy.mylio.global.util;

import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

@RequiredArgsConstructor
public class PasswordUtil {
    private static final PasswordEncoder encoder = new BCryptPasswordEncoder();

    public static String encode(String rawPassword){
        return encoder.encode(rawPassword);
    }

    public static boolean matches(String rawPassword, String encodedPassword){
        return encoder.matches(rawPassword, encodedPassword);
    }
}
