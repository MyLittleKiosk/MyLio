package com.ssafy.mylio.domain.account.entity;

import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.global.common.entity.BaseEntity;
import com.ssafy.mylio.global.common.status.BasicStatus;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;
@Entity
@Getter
@SuperBuilder
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Table(name = "account")
public class Account extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "store_id")
    private Store store;

    @Column(name = "username", nullable = false, length = 100)
    private String username;

    @Column(name = "password", nullable = false, length = 255)
    private String password;

    @Enumerated(EnumType.STRING)
    @Column(name = "role", nullable = false)
    private AccountRole role;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private BasicStatus status = BasicStatus.REGISTERED;

    public void update(String username, String password, BasicStatus status) {
        this.username = username;
        this.password = password;
        this.status = status;
    }

    public void delete() {
        this.status = BasicStatus.DELETED;
    }
}