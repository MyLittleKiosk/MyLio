package com.ssafy.mylio.domain.nutrition.repository;

import com.ssafy.mylio.domain.nutrition.entity.NutritionTemplate;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface NutritionTemplateRepository extends JpaRepository<NutritionTemplate, Integer> {

    @Query("""
        SELECT n FROM NutritionTemplate n
        WHERE (:keyword IS NULL OR :keyword = '' OR 
               LOWER(n.nameKr) LIKE LOWER(CONCAT('%', :keyword, '%')) OR 
               LOWER(n.nameEn) LIKE LOWER(CONCAT('%', :keyword, '%')))
        """)
    Page<NutritionTemplate> findAllByKeyword(@Param("keyword") String keyword, Pageable pageable);
}
