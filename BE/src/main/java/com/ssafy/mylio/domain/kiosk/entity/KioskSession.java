package com.ssafy.mylio.domain.kiosk.entity;

import com.ssafy.mylio.domain.account.entity.Account;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.global.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;

import java.time.LocalDateTime;

@Entity
@Getter
@SuperBuilder
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Table(name = "kiosk_session")
public class KioskSession extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "store_id", nullable = false)
    private Store store;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "account_id", nullable = false)
    private Account account;

    @Column(name = "start_order_number", nullable = false, length = 50)
    private String startOrderNumber;

    @Column(name = "name", length = 50)
    private String name;

    @Column(name = "is_active", nullable = false)
    private Boolean isActive;

    @Column(name = "started_at", nullable = false)
    private LocalDateTime startedAt;

    public void update(String name, Boolean isActive) {
        this.name = name;
        this.isActive = isActive;
    }

    public  void update(String name, String startOrder){
        this.name = name;
        this.startOrderNumber = startOrder;
    }

    public void updateActive(Boolean isActive) {
        this.isActive = isActive;
    }
}