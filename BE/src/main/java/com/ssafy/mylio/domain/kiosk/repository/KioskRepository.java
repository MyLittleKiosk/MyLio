package com.ssafy.mylio.domain.kiosk.repository;

import com.ssafy.mylio.domain.kiosk.entity.KioskSession;
import org.springframework.data.domain.Page;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import org.springframework.data.domain.Pageable;
import java.util.Optional;

@Repository
public interface KioskRepository extends JpaRepository<KioskSession,Integer> {
    Optional<KioskSession> findByStoreIdAndId(Integer storeId, Integer id);

    Optional<KioskSession> findByStoreIdAndName(Integer storeId, String name);

    //키워드 없을 때 검색
    Page<KioskSession> findByStoreId(Integer storeId, Pageable pageable);

    //키워드 있는 경우
    Page<KioskSession> findByStoreIdAndNameContainingIgnoreCase(Integer storeId,String keywork,Pageable pageable);
}

