package com.ssafy.mylio.domain.auth.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;

@Getter
public class LogoutRequest {
    @Schema(example = "1", description = "키오스크 아이디")
    private Integer kioskId;
}
