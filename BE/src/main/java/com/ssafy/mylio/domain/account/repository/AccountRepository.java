package com.ssafy.mylio.domain.account.repository;

import com.ssafy.mylio.domain.account.entity.Account;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface AccountRepository extends JpaRepository<Account,Integer> {
    @EntityGraph(attributePaths = "store")
    Optional<Account> findWithStoreById(Integer id);

    @EntityGraph(attributePaths = "store")
    Optional<Account> findWithStoreByEmail(String email);

    @Query("""
    SELECT a FROM Account a 
    JOIN FETCH a.store s 
    WHERE (:keyword IS NULL 
        OR LOWER(a.username) LIKE LOWER(CONCAT('%', :keyword, '%')) 
        OR LOWER(a.email) LIKE LOWER(CONCAT('%', :keyword, '%')) 
        OR LOWER(s.name) LIKE LOWER(CONCAT('%', :keyword, '%')))
    """)
    Page<Account> searchAccounts(@Param("keyword") String keyword, Pageable pageable);
}
