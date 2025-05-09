package com.ssafy.mylio.domain.order.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.StringJoiner;

/**
 * GPT 프롬프트 서비스
 * • 필수 옵션 누락 시 사용자에게 물어볼 "reply" 문자열을 생성
 * • 필요하면 OpenAI Chat API를 직접 호출해 더 자연스러운 문장으로 변환
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class GptPromptService {

    /** OpenAI Chat API endpoint */
    @Value("${openai.url:https://api.openai.com/v1}")
    private String openAiUrl;

    /** 사용 모델명 */
    @Value("${openai.model:gpt-3.5-turbo}")
    private String model;

    /** Bearer 토큰 */
    @Value("${spring.ai.openai.api-key}")
    private String apiKey;

    /* ------------------------------------------------------------------ */
    /*  1) 간단한 규칙 기반 프롬프트 빌더                                  */
    /* ------------------------------------------------------------------ */
    public String buildAskRequiredOptionPrompt(List<String> optionNames, String lang) {
        StringJoiner joiner = new StringJoiner(", ");
        optionNames.forEach(joiner::add);
        return switch (lang == null ? "KR" : lang.toUpperCase()) {
            case "EN" -> "Please choose the following required options: " + joiner;
            default     -> joiner + "는 필수 옵션입니다. " + joiner+ "를 선택해 주세요 !" ;
        };
    }

    /* ------------------------------------------------------------------ */
    /*  2) OpenAI Chat API 호출 (비동기)                                   */
    /* ------------------------------------------------------------------ */
    public Mono<String> refineWithGpt(String systemPrompt, String userPrompt) {
        String payload = """
            {
              \"model\": \"%s\",
              \"messages\": [
                {\"role\": \"system\", \"content\": \"%s\"},
                {\"role\": \"user\",   \"content\": \"%s\"}
              ]
            }
            """.formatted(model, escape(systemPrompt), escape(userPrompt));

        WebClient client = WebClient.builder()
                .baseUrl(openAiUrl)
                .defaultHeader("Authorization", "Bearer " + apiKey)
                .build();

        return client.post()
                .uri("/chat/completions")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(payload)
                .retrieve()
                .bodyToMono(String.class)
                .onErrorResume(e -> {
                    log.error("[GPT] API 호출 실패", e);
                    return Mono.just(userPrompt); // 실패 시 원본 프롬프트 사용
                });
    }

    /* JSON 문자열에 넣기 위한 이스케이프 헬퍼 */
    private String escape(String s) {
        return s == null ? "" : s.replace("\"", "\\\"");
    }
}
