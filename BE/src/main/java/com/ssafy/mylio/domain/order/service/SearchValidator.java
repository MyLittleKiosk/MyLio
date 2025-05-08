package com.ssafy.mylio.domain.order.service;

import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
@RequiredArgsConstructor
public class SearchValidator {
    public Mono<Void> validate(OrderResponseDto resp){
        return Mono.fromRunnable(()-> {
            resp.getContents().forEach(c-> {
                if(c.getMenuId()== null || c.getName()==null)
                    throw new CustomException(ErrorCode.MENU_NOT_FOUND);
            });
        });
    }
}
