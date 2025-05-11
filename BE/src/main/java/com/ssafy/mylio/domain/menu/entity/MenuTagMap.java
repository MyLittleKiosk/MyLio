package com.ssafy.mylio.domain.menu.entity;

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
@Table(name = "menu_tag_map")
public class MenuTagMap extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "menu_id", nullable = false)
    private Menu menu;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "store_id", nullable = false)
    private Store store;

    @Column(name = "tag_kr", nullable = false, length = 100)
    private String tagKr;

    @Column(name = "tag_en", nullable = false, length = 100)
    private String tagEn;

    public void update(String tagKr, String tagEn) {
        this.tagKr = tagKr;
        this.tagEn = tagEn;
    }
}