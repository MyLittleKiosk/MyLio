package com.ssafy.mylio.domain.menuIngredient.repository;

import com.ssafy.mylio.domain.menuIngredient.entity.MenuIngredient;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface MenuIngredientRepository extends JpaRepository<MenuIngredient, Integer> {
    List<MenuIngredient> findAllByMenuId(Integer menuId);
}
