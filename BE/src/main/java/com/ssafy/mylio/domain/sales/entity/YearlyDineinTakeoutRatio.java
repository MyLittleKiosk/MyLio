package com.ssafy.mylio.domain.sales.entity;

import com.ssafy.mylio.domain.order.entity.OrderStatus;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.global.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;

import java.math.BigDecimal;

@Entity
@Getter
@Table(name = "yearly_dinein_takeout_ratio")
@SuperBuilder
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class YearlyDineinTakeoutRatio extends BaseEntity {

    @ManyToOne
    @JoinColumn(name = "store_id", nullable = false)
    private Store store;

    @Column(name = "year", nullable = false)
    private Integer year;

    @Enumerated(EnumType.STRING)
    @Column(name = "type", nullable = false)
    private OrderStatus type;

    @Column(name = "ratio", nullable = false, precision = 5, scale = 2)
    private BigDecimal ratio;
}