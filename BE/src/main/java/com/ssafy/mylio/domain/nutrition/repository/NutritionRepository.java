package com.ssafy.mylio.domain.nutrition.repository;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.nutrition.entity.NutritionValue;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface NutritionRepository extends JpaRepository<NutritionValue, Integer> {
    List<NutritionValue> findAllByMenuId(Integer menuId);

    @Modifying(clearAutomatically=true)
    @Query("DELETE FROM NutritionValue nv WHERE nv.menu = :menu")
    void deleteByMenu(@Param("menu") Menu menu);

    @Query("""
              select nv
              from NutritionValue nv
                join fetch nv.nutrition nt
              where nv.menu.id = :menuId
            """)
    List<NutritionValue> findAllWithTemplateByMenuId(Integer menuId);

}
