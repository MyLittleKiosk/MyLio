package com.ssafy.mylio.domain.nutrition.repository;

import com.ssafy.mylio.domain.nutrition.entity.NutritionValue;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface NutritionRepository extends JpaRepository<NutritionValue, Integer> {
    List<NutritionValue> findAllByMenuId(Integer menuId);
}
