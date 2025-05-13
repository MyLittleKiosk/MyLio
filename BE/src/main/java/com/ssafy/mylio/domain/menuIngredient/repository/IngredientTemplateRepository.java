package com.ssafy.mylio.domain.menuIngredient.repository;

import com.ssafy.mylio.domain.menuIngredient.entity.IngredientTemplate;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface IngredientTemplateRepository extends JpaRepository<IngredientTemplate, Integer> {

    @Query("""
        SELECT it FROM IngredientTemplate it
        WHERE (:keyword IS NULL OR :keyword = '' OR
               LOWER(it.nameKr) LIKE LOWER(CONCAT('%', :keyword, '%')) OR
               LOWER(it.nameEn) LIKE LOWER(CONCAT('%', :keyword, '%')))
        """)
    Page<IngredientTemplate> findAllByKeyword(@Param("keyword") String keyword, Pageable pageable);
}
