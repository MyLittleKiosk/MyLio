package com.ssafy.mylio.domain.menu.repository;

import com.ssafy.mylio.domain.menu.entity.MenuTagMap;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface MenuTagMapRepository extends JpaRepository<MenuTagMap, Integer> {

    List<MenuTagMap> findByMenuIdIn(List<Integer> menuIds);
    List<MenuTagMap> findAllByMenuId(Integer menuId);
}
