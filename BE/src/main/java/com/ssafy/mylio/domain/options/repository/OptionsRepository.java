package com.ssafy.mylio.domain.options.repository;

import com.ssafy.mylio.domain.options.entity.Options;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OptionsRepository extends JpaRepository<Options, Integer> {
    @Query("""
    SELECT o FROM Options o
    WHERE o.store.id = :storeId
      AND o.status != com.ssafy.mylio.domain.options.entity.OptionStatus.DELETED
      AND (:keyword IS NULL OR LOWER(o.optionNameKr) LIKE LOWER(CONCAT('%', :keyword, '%'))
                           OR LOWER(o.optionNameEn) LIKE LOWER(CONCAT('%', :keyword, '%')))
""")
    Page<Options> findAllByStoreIdAndKeyword(@Param("storeId") Integer storeId,
                                             @Param("keyword") String keyword,
                                             Pageable pageable);

}
