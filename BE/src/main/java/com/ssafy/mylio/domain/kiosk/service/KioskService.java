package com.ssafy.mylio.domain.kiosk.service;

import com.ssafy.mylio.domain.account.entity.Account;
import com.ssafy.mylio.domain.account.entity.AccountRole;
import com.ssafy.mylio.domain.account.repository.AccountRepository;
import com.ssafy.mylio.domain.kiosk.dto.request.KioskCreateRequestDto;
import com.ssafy.mylio.domain.kiosk.dto.response.KioskCreateResponseDto;
import com.ssafy.mylio.domain.kiosk.entity.KioskSession;
import com.ssafy.mylio.domain.kiosk.repository.KioskRepository;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

import static java.time.LocalDateTime.now;

@Slf4j
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class KioskService {
    private final KioskRepository kioskRepository;
    private final StoreRepository storeRepository;
    private final AccountRepository accountRepository;

    @Transactional
    public KioskCreateResponseDto createKiosk(Integer userId,String userType, Integer storeId, KioskCreateRequestDto request){
        //역할이 STORE 아닌 경우 불가
        if (!userType.equals(AccountRole.STORE.getCode())) {
            throw new CustomException(ErrorCode.INVALID_ROLE)
                    .addParameter("userType",userType);
        }
        //계정 조회
        Account account = accountRepository.findWithStoreById(userId)
                .orElseThrow(() -> new CustomException(ErrorCode.ACOUNT_NOT_FOUND,"accountId",userId));

        //매장 조회
        Store store = storeRepository.findById(storeId)
                .orElseThrow(() -> new CustomException(ErrorCode.STORE_NOT_FOUND,"storeId",storeId));

        //그 이름으로 등록된 키오스크가 있는지 조회
        Optional<KioskSession> existingKiosk = kioskRepository.findByStoreIdAndName(store.getId(),request.getName());

        //있으면 return
        if(existingKiosk.isPresent()){
            throw new CustomException(ErrorCode.ALREADY_EXIST_KIOSK,"kiosk_name",request.getName());
        }

        //키오스크 등록
        KioskSession kioskSession = KioskSession.builder()
                .store(store)
                .account(account)
                .startOrderNumber(request.getStartOrder())
                .name(request.getName())
                .startedAt(now())
                .isActive(false)
                .build();

        //저장
        kioskRepository.save(kioskSession);

        return KioskCreateResponseDto.of(kioskSession);
    }
}
