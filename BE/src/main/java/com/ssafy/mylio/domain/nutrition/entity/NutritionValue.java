package com.ssafy.mylio.domain.nutrition.entity;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.global.common.entity.BaseEntity;
import com.ssafy.mylio.global.common.status.TrackableStatus;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;

import java.math.BigDecimal;

@Entity
@Getter
@SuperBuilder
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Table(name = "nutrition_value")
public class NutritionValue extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "store_id", nullable = false)
    private Store store;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "menu_id", nullable = false)
    private Menu menu;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "nutrition_id", nullable = false)
    private NutritionTemplate nutrition;

    @Column(name = "value", nullable = false, precision = 10, scale = 2)
    private BigDecimal value;

    @Enumerated(EnumType.STRING)
    @Column(name = "status")
    private TrackableStatus status = TrackableStatus.REGISTERED;

    public void update(BigDecimal value) {
        this.value = value;
        this.status = TrackableStatus.UPDATED;
    }

    public void delete() {
        this.status = TrackableStatus.DELETED;
    }
}