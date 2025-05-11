package com.ssafy.mylio.domain.order.service;

import com.ssafy.mylio.domain.menu.repository.MenuRepository;
import com.ssafy.mylio.domain.order.dto.response.ContentsResponseDto;
import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import com.ssafy.mylio.domain.order.util.OrderJsonMapper;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class SearchValidatorService {

    private final OrderJsonMapper mapper;
    private final MenuRepository menuRepository;

    public Mono<OrderResponseDto> validate(String pyJson, UserPrincipal user) {
        log.info("옵션 검증 로직 진입 : {}", pyJson);
        return Mono.fromCallable(() -> parseAndValidate(mapper.parse(pyJson, user), user))
                .subscribeOn(Schedulers.boundedElastic());
    }

    @Transactional(readOnly = true)
    protected OrderResponseDto parseAndValidate(OrderResponseDto order, UserPrincipal user) {

        Integer storeId = order.getStoreId();

        // storeId로 모든 메뉴 조회
        List<Integer> menuIds = menuRepository.findAllByStoreId(storeId).stream()
                .map(menu-> menu.getId())
                .toList();

        // contents의 menuId가 모두 유효한지 검증
        for (ContentsResponseDto c : order.getContents()) {
            Integer menuId = c.getMenuId();
            if (!menuIds.contains(menuId)) {
                throw new CustomException(ErrorCode.MENU_NOT_FOUND, "menuId", menuId);
            }
        }

        return order;
    }
}
