package com.ssafy.mylio.domain.order.service;

import com.ssafy.mylio.domain.menu.repository.MenuRepository;
import com.ssafy.mylio.domain.options.entity.MenuOptionMap;
import com.ssafy.mylio.domain.options.repository.MenuOptionRepository;
import com.ssafy.mylio.domain.order.dto.common.OptionsDto;
import com.ssafy.mylio.domain.order.dto.response.CartResponseDto;
import com.ssafy.mylio.domain.order.dto.response.ContentsResponseDto;
import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import com.ssafy.mylio.domain.order.util.OrderJsonMapper;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

@Service
@Slf4j
@RequiredArgsConstructor
public class PaymentValidatorService {

    private final OrderJsonMapper mapper;
    private final MenuRepository menuRepository;
    private final MenuOptionRepository menuOptionRepository;

    public Mono<OrderResponseDto> validate(String pyJson, UserPrincipal user) {
        log.info("결제 검증 로직 진입 : {}", pyJson);
        return Mono.fromCallable(() -> parseAndValidate(mapper.parse(pyJson, user), user))
                .subscribeOn(Schedulers.boundedElastic());
    }

    // 결제 검증 로직
    protected OrderResponseDto parseAndValidate(OrderResponseDto order, UserPrincipal user) {

        String screenState = order.getScreenState();

        if(order.getCart() == null || order.getCart().isEmpty()){
            throw new CustomException(ErrorCode.CART_IS_EMPTY);
        }

        if(screenState.equals("PAY")){
            payValidate(order);
        }

        List<CartResponseDto> fixedCart = order.getCart().stream()
                .map(this::validateCartItem)
                .toList();

        // cart에 있는 내용을 content에 넣기
        List<ContentsResponseDto> generateContents = null;
        if(screenState.equals("SELECT_PAY") || screenState.equals("CONFIRM")){
            generateContents = fixedCart.stream()
                    .map(cart-> ContentsResponseDto.builder()
                            .menuId(cart.getMenuId())
                            .quantity(cart.getQuantity())
                            .name(cart.getName())
                            .description(cart.getDescription())
                            .basePrice(cart.getBasePrice())
                            .totalPrice(cart.getTotalPrice())
                            .imageUrl(cart.getImageUrl())
                            .selectedOption(cart.getSelectedOptions())
                            .options(List.of())
                            .nutritionInfo(List.of())
                            .build())
                    .toList();
        }

        return order.toBuilder()
                .cart(fixedCart)
                .contents(generateContents != null ? generateContents : order.getContents())
                .build();
    }

    private CartResponseDto validateCartItem(CartResponseDto item) {
        Integer menuId = item.getMenuId();

        menuRepository.findById(menuId)
                .orElseThrow(()-> new CustomException(ErrorCode.MENU_NOT_FOUND,"menuId", menuId));

        // 옵션 매핑 검증
        List<MenuOptionMap> maps = menuOptionRepository.findAllWithDetailByMenuId(menuId);
        Map<Integer, List<MenuOptionMap>> optionMapGroup = maps.stream()
                .collect(Collectors.groupingBy(m-> m.getOptions().getId()));

        // DTO에 있는 옵션과 DB 옵션이 일치하는지 확인
        List<OptionsDto> fixedSelected = new ArrayList<>();

        for(OptionsDto dto : item.getSelectedOptions()){
            Integer optionId = dto.getOptionId();
            List<MenuOptionMap> validGroup = optionMapGroup.get(optionId);

            if(validGroup == null){
                throw new CustomException(ErrorCode.OPTION_NOT_FOUND,"optionId", optionId);
            }

            List<Integer> validDetailIds = validGroup.stream()
                    .map(m-> m.getOptionDetail().getId())
                    .toList();

            // selectedId가 누락되었거나 invalid한 경우 수정
            Integer selectedId = dto.getSelectedId();
            if(selectedId == null || !validDetailIds.contains(selectedId)){
                selectedId = dto.getOptionDetails().get(0).getOptionDetailId();
            }


            fixedSelected.add(dto.toBuilder()
                    .selectedId(selectedId)
                    .isSelected(dto.isSelected())
                    .build());
        }
        return item.toBuilder()
                .selectedOptions(fixedSelected)
                .build();

    }

    private void payValidate(OrderResponseDto order) {
        String paymentMethod = order.getPayment();
        Set<String> validMethods = Set.of("CARD", "MOBILE", "GIFT", "PAY");

        if (paymentMethod == null || paymentMethod.isBlank()) {
            throw new CustomException(ErrorCode.PAY_NOT_FOUND, "paymentMethod", paymentMethod);
        }

        if (!validMethods.contains(paymentMethod)) {
            throw new CustomException(ErrorCode.PAY_NOT_MATCH, "paymentMethod", paymentMethod);
        }

    }

}
