package com.ssafy.mylio.domain.category.repository;

import com.ssafy.mylio.domain.category.entity.Category;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface CategoryRepository extends JpaRepository<Category, Integer> {

    @Query("""
        SELECT c
        FROM Category c
        WHERE c.store.id = :storeId
        AND c.status != com.ssafy.mylio.domain.category.entity.Category.CategoryStatus.DELETED
        AND (:keyword IS NULL OR LOWER(c.nameKr) LIKE LOWER(CONCAT('%', :keyword, '%'))
        OR LOWER(c.nameEn) LIKE LOWER(CONCAT('%', :keyword, '%')))
            """)
    Page<Category> findAllByStoreIdAndKeyword(
            @Param("storeId") Integer storeId,
            @Param("keyword") String keyword,
            Pageable pageable);
}
