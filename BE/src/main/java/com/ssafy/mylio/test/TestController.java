package com.ssafy.mylio.test;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

public class TestController {
    public static void main(String[] args) {
        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
        String rawPassword = "qwer1234";
        String hashed = encoder.encode(rawPassword);
        System.out.println("secret password: " + hashed);
    }
}
