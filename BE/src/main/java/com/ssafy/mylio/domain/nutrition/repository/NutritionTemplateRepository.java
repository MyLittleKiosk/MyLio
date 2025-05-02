package com.ssafy.mylio.domain.nutrition.repository;

import com.ssafy.mylio.domain.nutrition.entity.NutritionTemplate;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface NutritionTemplateRepository extends JpaRepository<NutritionTemplate, Integer> {
}
