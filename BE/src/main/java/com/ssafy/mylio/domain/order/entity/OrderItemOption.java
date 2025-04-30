package com.ssafy.mylio.domain.order.entity;

import com.ssafy.mylio.domain.options.entity.OptionDetail;
import com.ssafy.mylio.global.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;

@Entity
@Getter
@SuperBuilder
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Table(name = "order_item_option")
public class OrderItemOption extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_item_id", nullable = false)
    private OrderItem orderItem;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "option_detail_id", nullable = false)
    private OptionDetail optionDetail;

    @Column(name = "price", nullable = false)
    private Integer price;
}