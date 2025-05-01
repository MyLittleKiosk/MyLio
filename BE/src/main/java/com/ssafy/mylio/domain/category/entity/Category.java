package com.ssafy.mylio.domain.category.entity;

import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.global.common.entity.BaseEntity;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
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

    @Builder.Default
    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private CategoryStatus status = CategoryStatus.REGISTERED;

    public enum CategoryStatus {
        REGISTERED, HIDDEN, DELETED;

        public static CategoryStatus from (String value){
            try {
                return CategoryStatus.valueOf(value.toUpperCase().trim());
            } catch (Exception e) {
                throw new CustomException(ErrorCode.INVALID_CATEGORY_STATUS, "status", value);
            }
        }
    }

    public void update(String nameKr, String nameEn, String status) {
        this.nameKr = nameKr;
        this.nameEn = nameEn;
        this.status = CategoryStatus.from(status);
    }

    public void hide() {
        this.status = CategoryStatus.HIDDEN;
    }

    public void delete() {
        this.status = CategoryStatus.DELETED;
    }
}