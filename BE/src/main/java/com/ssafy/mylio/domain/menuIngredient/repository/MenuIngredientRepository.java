package com.ssafy.mylio.domain.menuIngredient.repository;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.menuIngredient.entity.MenuIngredient;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MenuIngredientRepository extends JpaRepository<MenuIngredient, Integer> {
    List<MenuIngredient> findAllByMenuId(Integer menuId);

    @Modifying(clearAutomatically = true)
    @Query("DELETE FROM MenuIngredient mi WHERE mi.menu = :menu")
    void deleteByMenu(@Param("menu") Menu menu);

}
