package com.ssafy.mylio.global.common.entity;

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
@Table(name = "status_code")
public class StatusCode extends BaseEntity {

    @Column(name = "status", nullable = false, length = 100)
    private String status;
}