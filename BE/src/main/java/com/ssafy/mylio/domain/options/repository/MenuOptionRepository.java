package com.ssafy.mylio.domain.options.repository;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.options.entity.MenuOptionMap;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MenuOptionRepository extends JpaRepository<MenuOptionMap, Integer> {

    List<MenuOptionMap> findAllByMenuId(Integer menuId);

    @Modifying(clearAutomatically=true)
    @Query("DELETE FROM MenuOptionMap mo WHERE mo.menu = :menu")
    void deleteByMenu(@Param("menu") Menu menu);

    @Query("""
            select mom
            from   MenuOptionMap mom
              join fetch mom.options opt
              join fetch mom.optionDetail od
            where  mom.menu.id = :menuId
           """)
    List<MenuOptionMap> findAllWithDetailByMenuId(Integer menuId);

}
