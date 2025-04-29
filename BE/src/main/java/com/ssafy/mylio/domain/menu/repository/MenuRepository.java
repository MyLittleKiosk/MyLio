package com.ssafy.mylio.domain.menu.repository;

import com.ssafy.mylio.domain.menu.entity.Menu;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;


public interface MenuRepository extends JpaRepository<Menu, Integer> {

    @Query("""
            SELECT m
            FROM Menu m
            WHERE m.store.id = :storeId
              AND (:categoryId IS NULL OR m.category.id = :categoryId)
        """)
    Page<Menu> findByStoreIdAndOptionalCategoryId(
            @Param("storeId") Integer storeId,
            @Param("categoryId") Integer categoryId,
            Pageable pageable
    );
}
