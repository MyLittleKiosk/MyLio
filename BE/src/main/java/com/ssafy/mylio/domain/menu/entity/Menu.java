package com.ssafy.mylio.domain.menu.entity;

import com.ssafy.mylio.domain.category.entity.Category;
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
@Table(name = "menu")
public class Menu extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id")
    private Category category;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "store_id", nullable = false)
    private Store store;

    @Column(name = "name_kr", nullable = false, length = 100)
    private String nameKr;

    @Column(name = "name_en", nullable = false, length = 100)
    private String nameEn;

    @Column(name = "description", nullable = false, length = 255)
    private String description;

    @Column(name = "price", nullable = false)
    private Integer price;

    @Column(name = "image_url", length = 255)
    private String imageUrl;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private MenuStatus status = MenuStatus.SELLING;

    public void update(Category category, String nameKr, String nameEn,
                       String description, Integer price, String imageUrl) {
        this.category = category;
        this.nameKr = nameKr;
        this.nameEn = nameEn;
        this.description = description;
        this.price = price;
        this.imageUrl = imageUrl;
    }

    public void updateStatus(MenuStatus status) {
        this.status = status;
    }

    public void soldOut() {
        this.status = MenuStatus.SOLD_OUT;
    }

    public void hide() {
        this.status = MenuStatus.HIDDEN;
    }

    public void delete() {
        this.status = MenuStatus.DELETED;
    }
}