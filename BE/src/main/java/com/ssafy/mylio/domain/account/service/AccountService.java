package com.ssafy.mylio.domain.account.service;

import com.ssafy.mylio.domain.account.dto.request.AccountCreateRequest;
import com.ssafy.mylio.domain.account.dto.response.AccountCreateResponseDto;
import com.ssafy.mylio.domain.account.entity.Account;
import com.ssafy.mylio.domain.account.entity.AccountRole;
import com.ssafy.mylio.domain.account.repository.AccountRepository;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.global.common.status.BasicStatus;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class AccountService {
    private final AccountRepository accountRepository;
    private final StoreRepository storeRepository;

    @Transactional
    public AccountCreateResponseDto createAccount(String userType, AccountCreateRequest request) {
        //역할이 SUPER가 아닌 경우 불가
        if (!userType.equals(AccountRole.SUPER.getCode())) {
            throw new CustomException(ErrorCode.INVALID_ROLE)
                    .addParameter("userType",userType);
        }

        Integer storeId = request.getStoreId();
        //store 검증
        if (storeId == null) {
            log.debug("storeId is null");
            throw new CustomException(ErrorCode.STORE_NOT_FOUND);
        }
        Store store = storeRepository.findById(storeId)
                .orElseThrow(() -> new CustomException(ErrorCode.STORE_NOT_FOUND));

        AccountRole role = AccountRole.STORE;

        // 엔티티 생성
        Account account = Account.builder()
                .store(store)
                .username(request.getUserName())
                .password(request.getPassword())
                .role(role)
                .status(BasicStatus.REGISTERED)
                .build();
        //저장
        Account saved = accountRepository.save(account);

        return AccountCreateResponseDto.of(account);

    }
}
