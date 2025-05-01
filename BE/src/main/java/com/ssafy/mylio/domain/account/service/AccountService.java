package com.ssafy.mylio.domain.account.service;

import com.ssafy.mylio.domain.account.dto.request.AccountCreateRequest;
import com.ssafy.mylio.domain.account.dto.request.AccountModifyRequestDto;
import com.ssafy.mylio.domain.account.dto.response.AccountDetailResponseDto;
import com.ssafy.mylio.domain.account.dto.response.AccountListResponseDto;
import com.ssafy.mylio.domain.account.dto.response.AccountModifyResponse;
import com.ssafy.mylio.domain.account.entity.Account;
import com.ssafy.mylio.domain.account.entity.AccountRole;
import com.ssafy.mylio.domain.account.repository.AccountRepository;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.global.common.CustomPage;
import com.ssafy.mylio.global.common.status.BasicStatus;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.data.domain.Pageable;


@Slf4j
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class AccountService {
    private final AccountRepository accountRepository;
    private final StoreRepository storeRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    public void createAccount(String userType, AccountCreateRequest request) {
        //역할이 SUPER가 아닌 경우 불가
        if (!userType.equals(AccountRole.SUPER.getCode())) {
            throw new CustomException(ErrorCode.INVALID_ROLE)
                    .addParameter("userType",userType);
        }

        //Store 정보 저장
        Store store = saveStoreInfo(request);

        // 비밀번호 암호화
        String encodedPassword = passwordEncoder.encode(request.getEmail());
        // 엔티티 생성
        Account account = Account.builder()
                .store(store)
                .email(request.getEmail())
                .username(request.getUserName())
                .password(encodedPassword)
                .role(AccountRole.STORE)
                .status(BasicStatus.REGISTERED)
                .build();
        //저장
        accountRepository.save(account);

    }
    @Transactional
    public AccountModifyResponse modifyAccount(Integer userId, String userType, AccountModifyRequestDto request){
        //Super 권한만 가능
        if(!userType.equals(AccountRole.SUPER.getCode())){
            throw new CustomException(ErrorCode.INVALID_ROLE)
                    .addParameter("userType",userType);
        }

        Integer adminId = request.getUserId();

        //계정 정보 가져오기
        Account account = accountRepository.findWithStoreById(adminId)
                .orElseThrow(() -> new CustomException(ErrorCode.ACOUNT_NOT_FOUND));

        //계정 enum으로 변경
        BasicStatus status = request.getStatus().equals(BasicStatus.REGISTERED.getCode())?
                BasicStatus.REGISTERED : BasicStatus.DELETED;
        //정보 업데이트 및 저장
        account.update(request.getUserName(),request.getPassword(),status);
        accountRepository.save(account);

        return AccountModifyResponse.of(account);
    }

    private Store saveStoreInfo(AccountCreateRequest request){
        Store store = Store.builder()
                .name(request.getStoreName())
                .status(BasicStatus.REGISTERED)
                .address(request.getAddress())
                .build();
        store = storeRepository.save(store);

        Integer storeId = store.getId();
        log.info("store id {}",storeId);
        //store 검증
        if (store == null || store.getId() == null) {
            log.error("Failed to save store: {}", request.getStoreName());
            throw new CustomException(ErrorCode.STORE_NOT_FOUND,"",request.getStoreName());
        }
        return store;
    }


    public CustomPage<AccountListResponseDto> getAccountList(String userType, String keyword, Pageable pageable){
        //역할이 SUPER가 아닌 경우 불가
        if (!userType.equals(AccountRole.SUPER.getCode())) {
            throw new CustomException(ErrorCode.INVALID_ROLE)
                    .addParameter("userType",userType);
        }
        Page<Account> accounts = accountRepository.searchAccounts(keyword, pageable);
        Page<AccountListResponseDto> dtoPage = accounts.map(AccountListResponseDto::of);
        return new CustomPage<>(dtoPage);
    }

    public AccountDetailResponseDto getAccountDetail(Integer userId, Integer storeId, String userType){
        //역할이 STORE가 아닌 경우 불가
        if (!userType.equals(AccountRole.STORE.getCode())) {
            throw new CustomException(ErrorCode.INVALID_ROLE)
                    .addParameter("userType",userType);
        }

        Account account = accountRepository.findById(userId)
                .orElseThrow(() -> new CustomException(ErrorCode.ACOUNT_NOT_FOUND)
                        .addParameter("userId",userId));

        Store store = storeRepository.findById(storeId)
                .orElseThrow(() -> new CustomException(ErrorCode.STORE_NOT_FOUND)
                        .addParameter("storeId", storeId));

        return AccountDetailResponseDto.of(account,store);
    }
}
