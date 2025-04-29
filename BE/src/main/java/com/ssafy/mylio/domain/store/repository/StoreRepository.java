package com.ssafy.mylio.domain.store.repository;

import com.ssafy.mylio.domain.store.entity.Store;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StoreRepository extends JpaRepository<Store,Integer> {
}
