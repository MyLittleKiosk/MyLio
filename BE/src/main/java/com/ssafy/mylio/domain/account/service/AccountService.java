package com.ssafy.mylio.domain.account.service;

import com.ssafy.mylio.domain.account.dto.request.AccountCreateRequest;
import com.ssafy.mylio.domain.account.dto.request.AccountModifyRequestDto;
import com.ssafy.mylio.domain.account.dto.request.PasswordRequestDto;
import com.ssafy.mylio.domain.account.dto.request.ModifyPasswordRequest;
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

import java.security.SecureRandom;


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
    public AccountModifyResponse modifyAccount(Integer userId,Integer storeId, String userType, AccountModifyRequestDto request){
        //Store 권한만 가능
        if(!userType.equals(AccountRole.STORE.getCode())){
            throw new CustomException(ErrorCode.INVALID_ROLE)
                    .addParameter("userType",userType);
        }

        //계정 정보 가져오기
        Account account = accountRepository.findWithStoreById(userId)
                .orElseThrow(() -> new CustomException(ErrorCode.ACOUNT_NOT_FOUND));

        //정보 업데이트 및 저장
        account.update(request.getUserName(),request.getEmail());

        //매장 정보 가져오기
        Store store = storeRepository.findById(storeId)
                .orElseThrow(()-> new CustomException(ErrorCode.STORE_NOT_FOUND));

        store.update(request.getStoreName(),request.getAddress());

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

    @Transactional
    public void deleteAccount(Integer accountId, String userType){
        //Super 권한만 가능
        if(!userType.equals(AccountRole.SUPER.getCode())){
            throw new CustomException(ErrorCode.INVALID_ROLE)
                    .addParameter("userType",userType);
        }
        //usrID로 매장 계정 정보 가져오기
        Account account = accountRepository.findWithStoreById(accountId)
                .orElseThrow(() -> new CustomException(ErrorCode.ACOUNT_NOT_FOUND));
        //매장 삭제하기
        Store store = storeRepository.findById(account.getStore().getId())
                .orElseThrow(()-> new CustomException(ErrorCode.STORE_NOT_FOUND));

        if(store.getStatus() == BasicStatus.DELETED){
            throw new CustomException(ErrorCode.STORE_DELETED,"storeId",store.getId());
        }

        store.delete();
        //계정 삭제하기
        account.delete();

    }
    public String findPassword(PasswordRequestDto request){
        //이메일이랑 이름으로 조회(시큐리티 설정하기)
        Account account = accountRepository.findWithStoreByEmail(request.getEmail())
                .orElseThrow(() -> new CustomException(ErrorCode.FORBIDDEN_AUTH,"username",request.getUsername())
                        .addParameter("email",request.getEmail()));

        //이름이 틀린 경우 접근 불가
        if(!account.getUsername().equals(request.getUsername())){
            throw new CustomException(ErrorCode.FORBIDDEN_AUTH,"username",request.getUsername())
                    .addParameter("email",request.getEmail());
        }

        //삭제된 계정일경우 접근 불가
        if(account.getStatus() == BasicStatus.DELETED){
            throw new CustomException(ErrorCode.ACOUNT_NOT_FOUND,"status",BasicStatus.DELETED.getCode());
        }

        //비밀번호 8자리 난수로 생성
        String newPassword = generateRandomPassword();

        //암호화 후 db 저장
        String encodedPW = passwordEncoder.encode(newPassword);
        account.update(encodedPW);

        //비밀번호 전달
        return newPassword;
    }

    private String generateRandomPassword() {
        final String chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*";
        SecureRandom random = new SecureRandom();
        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < 8; i++) {
            int randomIndex = random.nextInt(chars.length());
            sb.append(chars.charAt(randomIndex));
        }
        return sb.toString();

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

    @Transactional
    public void modifyPW(Integer userId, String userType, ModifyPasswordRequest request){

        //계정 조회
        Account account = accountRepository.findById(userId)
                .orElseThrow(()-> new CustomException(ErrorCode.ACOUNT_NOT_FOUND,"userId",userId));

        //현재 비밀번호가 맞는지 조회
        if(!passwordEncoder.matches(request.getNowPw(), account.getPassword())){
            throw new CustomException(ErrorCode.FORBIDDEN_AUTH);
        }

        //새로운 비밀번호 암호화 후 저장
        String encodedPW = passwordEncoder.encode(request.getNewPw());

        account.update(encodedPW);
    }
}
