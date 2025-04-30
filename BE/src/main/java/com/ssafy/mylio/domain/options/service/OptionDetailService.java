package com.ssafy.mylio.domain.options.service;

import com.ssafy.mylio.domain.options.dto.request.OptionDetailRequestDto;
import com.ssafy.mylio.domain.options.entity.OptionDetail;
import com.ssafy.mylio.domain.options.repository.OptionDetailRepository;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class OptionDetailService {

    private final OptionDetailRepository optionDetailRepository;
    private final StoreRepository storeRepository;

    @Transactional
    public void deleteOptionDetail(Integer storeId, Integer optionDetailId){
        Store store = getStoreId(storeId);
        OptionDetail optionDetail = optionDetailRepository.findById(optionDetailId)
                .orElseThrow(()-> new CustomException(ErrorCode.OPTION_DETAIL_NOT_FOUND, "optionDetailId", optionDetailId));

        if (!optionDetail.getOptions().getStore().getId().equals(storeId)) {
            throw new CustomException(ErrorCode.OPTION_STORE_NOT_MATCH, "optionDetailId", optionDetailId);
        }

        optionDetail.delete();
    }

    @Transactional
    public void addOptionDetail(Integer storeId, Integer optionId, OptionDetailRequestDto optionDetailRequestDto){

    }

    private Store getStoreId(Integer storeId){
        return storeRepository.findById(storeId)
                .orElseThrow(()-> new CustomException(ErrorCode.STORE_NOT_FOUND, "storeId", storeId));
    }
}
