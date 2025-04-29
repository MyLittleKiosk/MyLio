package com.ssafy.mylio.domain.options.repository;

import com.ssafy.mylio.domain.options.entity.MenuOptionMap;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface MenuOptionRepository extends JpaRepository<MenuOptionMap, Integer> {

    List<MenuOptionMap> findAllByMenuId(Integer menuId);
}
