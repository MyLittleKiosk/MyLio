package com.ssafy.mylio.domain.payment.entity;

import com.ssafy.mylio.domain.order.entity.Orders;
import com.ssafy.mylio.domain.payment.entity.PaymentMethod;
import com.ssafy.mylio.domain.payment.entity.PaymentStatus;
import com.ssafy.mylio.domain.store.entity.Store;
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
@Table(name = "payment")
public class Payment extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "store_id", nullable = false)
    private Store store;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    private Orders order;

    @Enumerated(EnumType.STRING)
    @Column(name = "payment_method", nullable = false)
    private PaymentMethod paymentMethod;

    @Column(name = "amount", nullable = false)
    private Integer amount;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private PaymentStatus status = PaymentStatus.READY;

    @Column(name = "reason", length = 255)
    private String reason;

    @Column(name = "tid", nullable = false, length = 255)
    private String tid;

    @Column(name = "cid", nullable = false, length = 50)
    private String cid;

    public void updateStatus(PaymentStatus status, String reason) {
        this.status = status;
        this.reason = reason;
    }
}