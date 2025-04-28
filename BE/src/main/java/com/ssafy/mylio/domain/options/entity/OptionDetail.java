package com.ssafy.mylio.domain.options.entity;

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
@Table(name = "option_detail")
public class OptionDetail extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "option_id", nullable = false)
    private Options options;

    @Column(name = "value", nullable = false, length = 100)
    private String value;

    @Column(name = "additional_price")
    private Integer additionalPrice;

    public void update(String value, Integer additionalPrice) {
        this.value = value;
        this.additionalPrice = additionalPrice;
    }
}