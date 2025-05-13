package com.ssafy.mylio.domain.order.service;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.menu.repository.MenuRepository;
import com.ssafy.mylio.domain.options.entity.OptionDetail;
import com.ssafy.mylio.domain.options.repository.OptionDetailRepository;
import com.ssafy.mylio.domain.order.dto.common.OptionsDto;
import com.ssafy.mylio.domain.order.dto.response.CartResponseDto;
import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import com.ssafy.mylio.domain.order.entity.OrderItem;
import com.ssafy.mylio.domain.order.entity.OrderItemOption;
import com.ssafy.mylio.domain.order.entity.Orders;
import com.ssafy.mylio.domain.order.repository.OrderItemOptionRepository;
import com.ssafy.mylio.domain.order.repository.OrderItemRepository;
import com.ssafy.mylio.domain.order.repository.OrdersRepository;
import com.ssafy.mylio.domain.payment.entity.PaymentMethod;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class OrderService {

    private final OrdersRepository orderRepository;
    private final StoreRepository storeRepository;
    private final MenuRepository menuRepository;
    private final OrderItemRepository orderItemRepository;
    private final OrderItemOptionRepository orderItemOptionRepository;
    private final OptionDetailRepository optionDetailRepository;

    /* 옵션 검증 완료 → 장바구니 업데이트 등 */
    public Mono<OrderResponseDto> handleOrder(OrderResponseDto resp, UserPrincipal user) {
        // 예: totalPrice 재계산, cart 에 push
        return Mono.just(resp);
    }

    /* PAY 단계 */
    @Transactional
    public Mono<OrderResponseDto> handlePayment(OrderResponseDto resp, UserPrincipal user) {

        // Orders 저장
        Store store = storeRepository.findById(resp.getStoreId())
                .orElseThrow(()-> new CustomException(ErrorCode.STORE_NOT_FOUND,"storeId", resp.getStoreId()));

        Orders orders = Orders.builder()
                .store(store)
                .paymentMethod(PaymentMethod.fromCode(resp.getPayment()))
                .totalPrice(resp.getCart().stream().mapToInt(CartResponseDto::getTotalPrice).sum())
                .isToGo(true)
                .build();

        orderRepository.save(orders);

        // OrderItem, OrderItemOption 저장
        for(CartResponseDto cartResponseDto : resp.getCart()){

            Menu menu = menuRepository.findById(cartResponseDto.getMenuId())
                    .orElseThrow(()-> new CustomException(ErrorCode.MENU_NOT_FOUND,"menuId", cartResponseDto.getMenuId()));

            OrderItem orderItem = OrderItem.builder()
                    .menu(menu)
                    .order(orders)
                    .quantity(cartResponseDto.getQuantity())
                    .price(cartResponseDto.getTotalPrice())
                    .build();

            orderItemRepository.save(orderItem);

            // OrderItemOption 저장
            for(OptionsDto optionsDto : cartResponseDto.getSelectedOptions()){

                OptionDetail optionDetail = optionDetailRepository.findById(optionsDto.getOptionDetails().get(0).getOptionDetailId())
                        .orElseThrow(()-> new CustomException(ErrorCode.OPTION_DETAIL_NOT_FOUND,"optionDetailId",optionsDto.getOptionDetails().get(0).getOptionDetailId()));

                OrderItemOption orderItemOption = OrderItemOption.builder()
                        .orderItem(orderItem)
                        .optionDetail(optionDetail)
                        .price(orders.getTotalPrice())
                        .build();

                orderItemOptionRepository.save(orderItemOption);
            }
        }

        return Mono.just(resp);
    }

    @Transactional
    public Mono<Void> saveOrderAfterKakaoPay(Integer storeId, List<CartResponseDto> cart) {

        return Mono.fromRunnable(() -> {
            // 1. 매장 조회
            Store store = storeRepository.findById(storeId)
                    .orElseThrow(() -> new CustomException(ErrorCode.STORE_NOT_FOUND, "storeId", storeId));

            // 2. Orders 저장
            Orders orders = Orders.builder()
                    .store(store)
                    .paymentMethod(PaymentMethod.PAY)
                    .totalPrice(cart.stream().mapToInt(CartResponseDto::getTotalPrice).sum())
                    .isToGo(true)
                    .build();

            orderRepository.save(orders);

            // 3. Cart → OrderItem + OrderItemOption 매핑
            for (CartResponseDto cartItem : cart) {
                Menu menu = menuRepository.findById(cartItem.getMenuId())
                        .orElseThrow(() -> new CustomException(ErrorCode.MENU_NOT_FOUND, "menuId", cartItem.getMenuId()));

                OrderItem orderItem = OrderItem.builder()
                        .order(orders)
                        .menu(menu)
                        .price(cartItem.getTotalPrice())
                        .quantity(cartItem.getQuantity())
                        .build();

                orderItemRepository.save(orderItem);

                for (OptionsDto optionsDto : cartItem.getSelectedOptions()) {
                    OptionDetail optionDetail = optionDetailRepository.findById(
                                    optionsDto.getOptionDetails().get(0).getOptionDetailId())
                            .orElseThrow(() -> new CustomException(ErrorCode.OPTION_DETAIL_NOT_FOUND,
                                    "optionDetailId", optionsDto.getOptionDetails().get(0).getOptionDetailId()));

                    OrderItemOption orderItemOption = OrderItemOption.builder()
                            .orderItem(orderItem)
                            .optionDetail(optionDetail)
                            .price(orderItem.getPrice()) // 옵션 가격이 orders 가격과 동일한 구조면 유지
                            .build();

                    orderItemOptionRepository.save(orderItemOption);
                }
            }
        }).then(); // Mono<Void> 리턴
    }

}
