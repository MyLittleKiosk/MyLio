package com.ssafy.mylio.domain.menu.repository;

import com.ssafy.mylio.domain.menu.entity.Menu;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MenuRepository extends JpaRepository<Menu, Integer> {

    @Query("""
            SELECT m
            FROM Menu m
            WHERE m.store.id = :storeId
            AND m.status!=  'DELETED'
            """)
    List<Menu> findAllByStoreId(@Param("storeId")  Integer storeId);

    @Query("""
    SELECT m
    FROM Menu m
    WHERE m.store.id = :storeId
      AND m.status != com.ssafy.mylio.domain.menu.entity.MenuStatus.DELETED
      AND (:categoryId IS NULL OR m.category.id = :categoryId)
      AND (:keyword IS NULL OR LOWER(m.nameKr) LIKE LOWER(CONCAT('%', :keyword, '%'))
                             OR LOWER(m.nameEn) LIKE LOWER(CONCAT('%', :keyword, '%')))
""")
    Page<Menu> findByStoreIdAndOptionalCategoryIdAndKeyword(
            @Param("storeId") Integer storeId,
            @Param("categoryId") Integer categoryId,
            @Param("keyword") String keyword,
            Pageable pageable
    );
}
