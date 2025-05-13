package com.ssafy.mylio.domain.payment.dto.request;

import com.ssafy.mylio.domain.order.dto.response.CartResponseDto;
import lombok.Data;

import java.util.List;

@Data
public class KakaoPayApproveRequestDto {
    private String orderId;
    private String pgToken;
    private List<CartResponseDto> cart;
}
