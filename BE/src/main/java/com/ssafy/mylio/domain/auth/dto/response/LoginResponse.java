package com.ssafy.mylio.domain.auth.dto.response;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(oneOf = {SuperInfoResponseDto.class, StoreInfoResponseDto.class})

public interface LoginResponse {
}
