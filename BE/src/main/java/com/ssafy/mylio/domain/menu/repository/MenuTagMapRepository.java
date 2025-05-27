package com.ssafy.mylio.domain.menu.repository;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.menu.entity.MenuTagMap;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MenuTagMapRepository extends JpaRepository<MenuTagMap, Integer> {

    List<MenuTagMap> findByMenuIdIn(List<Integer> menuIds);
    List<MenuTagMap> findAllByMenuId(Integer menuId);

    @Modifying(clearAutomatically=true)
    @Query("DELETE FROM MenuTagMap m WHERE m.menu = :menu")
    void deleteByMenu(@Param("menu") Menu menu);
}
