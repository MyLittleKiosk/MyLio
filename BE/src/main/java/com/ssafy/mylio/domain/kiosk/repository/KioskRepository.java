package com.ssafy.mylio.domain.kiosk.repository;

import com.ssafy.mylio.domain.kiosk.entity.KioskSession;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface KioskRepository extends JpaRepository<KioskSession,Integer> {
    Optional<KioskSession> findByStoreIdAndId(Integer storeId, Integer id);
}

