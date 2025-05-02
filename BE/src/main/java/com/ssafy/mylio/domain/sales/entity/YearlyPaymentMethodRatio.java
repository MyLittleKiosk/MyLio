package com.ssafy.mylio.domain.sales.entity;

import com.ssafy.mylio.domain.payment.entity.PaymentMethod;
import com.ssafy.mylio.domain.payment.entity.PaymentStatus;
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
@Table(name = "yearly_payment_method_ratio")
@SuperBuilder
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class YearlyPaymentMethodRatio extends BaseEntity {

    @ManyToOne
    @JoinColumn(name = "store_id", nullable = false)
    private Store store;

    @Column(name = "year", nullable = false)
    private Integer year;

    @Enumerated(EnumType.STRING)
    @Column(name = "method", nullable = false)
    private PaymentMethod method;

    @Column(name = "ratio", nullable = false, precision = 5, scale = 2)
    private BigDecimal ratio;
}