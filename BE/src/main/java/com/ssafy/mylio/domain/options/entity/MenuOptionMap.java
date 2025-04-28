package com.ssafy.mylio.domain.options.entity;

import com.ssafy.mylio.domain.menu.entity.Menu;
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
@Table(name = "menu_option_map")
public class MenuOptionMap extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "menu_id", nullable = false)
    private Menu menu;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "option_id", nullable = false)
    private Options options;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "option_detail_id", nullable = false)
    private OptionDetail optionDetail;

    @Column(name = "is_required", nullable = false)
    private Boolean isRequired;

    public void update(Boolean isRequired) {
        this.isRequired = isRequired;
    }
}