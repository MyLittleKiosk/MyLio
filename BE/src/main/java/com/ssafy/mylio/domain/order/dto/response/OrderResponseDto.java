package com.ssafy.mylio.domain.order.dto.response;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder(toBuilder = true)
public class OrderResponseDto {
    @Schema(example = "1")
    private Integer storeId;
    @Schema(example = "배닐라 라떼 하나 어이스로 주세요")
    private String preText;
    @Schema(example = "바닐라라떼 하나 아이스로 주세요")
    private String postText;
    @Schema(example = "바닐라 라떼 사이즈는 뭘로 하시겠어요?")
    private String reply;
    @Schema(example = "ORDER")
    private String screenState;
    @Schema(example = "KR")
    private String language;
    @Schema(example = "A101")
    private String sessionId;
    @Schema(example = "CARD")
    private String payment;
    private List<CartResponseDto> cart;
    private List<ContentsResponseDto> contents;
}
