package com.ssafy.mylio;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class MylioApplication {

	public static void main(String[] args) {
		SpringApplication.run(MylioApplication.class, args);
	}

}
