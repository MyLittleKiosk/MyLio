package com.ssafy.mylio.domain.menuIngredient.entity;

import com.ssafy.mylio.global.common.entity.BaseEntity;
import com.ssafy.mylio.global.common.status.TrackableStatus;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;

@Entity
@Getter
@SuperBuilder
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Table(name = "ingredient_template")
public class IngredientTemplate extends BaseEntity {

    @Column(name = "name_kr", nullable = false, length = 100)
    private String nameKr;

    @Column(name = "name_en", nullable = false, length = 100)
    private String nameEn;

    @Enumerated(EnumType.STRING)
    @Column(name = "status")
    private TrackableStatus status = TrackableStatus.REGISTERED;

    public void update(String nameKr, String nameEn) {
        this.nameKr = nameKr;
        this.nameEn = nameEn;
        this.status = TrackableStatus.UPDATED;
    }

    public void delete() {
        this.status = TrackableStatus.DELETED;
    }
}