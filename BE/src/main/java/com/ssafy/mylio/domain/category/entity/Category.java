package com.ssafy.mylio.domain.category.entity;

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
@Table(name = "category")
public class Category extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "store_id", nullable = false)
    private Store store;

    @Column(name = "name_kr", nullable = false, length = 100)
    private String nameKr;

    @Column(name = "name_en", nullable = false, length = 100)
    private String nameEn;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private CategoryStatus status = CategoryStatus.REGISTERED;

    public enum CategoryStatus {
        REGISTERED, HIDDEN, DELETED
    }

    public void update(String nameKr, String nameEn) {
        this.nameKr = nameKr;
        this.nameEn = nameEn;
    }

    public void hide() {
        this.status = CategoryStatus.HIDDEN;
    }

    public void delete() {
        this.status = CategoryStatus.DELETED;
    }
}