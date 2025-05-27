package com.ssafy.mylio.domain.order.entity;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.global.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;

@Entity
@Getter
@SuperBuilder
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Table(name = "order_item")
public class OrderItem extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "menu_id", nullable = false)
    private Menu menu;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    private Orders order;

    @Column(name = "price", nullable = false)
    private Integer price;

    @Builder.Default
    @Column(name = "quantity", nullable = false)
    private Integer quantity = 1;
}