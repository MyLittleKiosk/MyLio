package com.ssafy.mylio.domain.order.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class OrderRequestDto {
    @Schema(example = "배닐라 라떼 하나 어이스로 주세요")
    private String text;
    @Schema(example = "ORDER")
    private String screenState;
    @Schema(example = "KR")
    private String language;
    @Schema(example = "A101")
    private String sessionId;
    @Schema(example = "2")
    private Integer storeId;
    private List<CartRequestDto> carts;
    private List<ContentRequestDto> contents;
}
