package com.ssafy.mylio.domain.options.entity;

import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.global.common.entity.BaseEntity;
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
@Table(name = "options")
public class Options extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "store_id", nullable = false)
    private Store store;

    @Column(name = "option_name_kr", nullable = false, length = 100)
    private String optionNameKr;

    @Column(name = "option_name_en", nullable = false, length = 100)
    private String optionNameEn;

    @Builder.Default
    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private OptionStatus status = OptionStatus.REGISTERED;

    public void update(String optionNameKr, String optionNameEn, String status) {
        this.optionNameKr = optionNameKr;
        this.optionNameEn = optionNameEn;
        this.status = OptionStatus.fromCode(status);
    }

    public void delete(){this.status = OptionStatus.DELETED;}
}