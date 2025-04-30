package com.ssafy.mylio.domain.nutrition.entity;

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
@Table(name = "nutrition_template")
public class NutritionTemplate extends BaseEntity {

    @Column(name = "name_kr", nullable = false, length = 100)
    private String nameKr;

    @Column(name = "name_en", nullable = false, length = 100)
    private String nameEn;

    @Column(name = "unit_type", nullable = false, length = 20)
    private String unitType;

    public void update(String nameKr, String nameEn, String unitType) {
        this.nameKr = nameKr;
        this.nameEn = nameEn;
        this.unitType = unitType;
    }
}