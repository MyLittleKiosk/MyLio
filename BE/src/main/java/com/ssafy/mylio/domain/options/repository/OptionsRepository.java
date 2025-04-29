package com.ssafy.mylio.domain.options.repository;

import com.ssafy.mylio.domain.options.entity.Options;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface OptionsRepository extends JpaRepository<Options, Integer> {
    List<Options> findAllByStoreId(Integer storeId);
}
