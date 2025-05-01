package com.ssafy.mylio.domain.account.repository;

import com.ssafy.mylio.domain.account.entity.Account;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface AccountRepository extends JpaRepository<Account,Integer> {
    @EntityGraph(attributePaths = "store")
    Optional<Account> findWithStoreById(Integer id);

    @EntityGraph(attributePaths = "store")
    Optional<Account> findWithStoreByEmail(String email);
}
