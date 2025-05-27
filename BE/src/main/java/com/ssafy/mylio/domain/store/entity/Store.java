package com.ssafy.mylio.domain.store.entity;

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
@Table(name = "store")
public class Store extends BaseEntity {

    @Column(name = "name", nullable = false, length = 100)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = true)
    private BasicStatus status = BasicStatus.REGISTERED;

    @Column(name = "address", nullable = false, length = 100)
    private String address;

    public void update(String name, String address) {
        this.name = name;
        this.address = address;
    }

    public void delete() {
        this.status = BasicStatus.DELETED;
    }
}