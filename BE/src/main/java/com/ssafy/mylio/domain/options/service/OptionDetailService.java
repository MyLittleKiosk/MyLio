package com.ssafy.mylio.domain.options.service;

import com.ssafy.mylio.domain.options.dto.request.OptionDetailRequestDto;
import com.ssafy.mylio.domain.options.dto.request.OptionDetailUpdateRequestDto;
import com.ssafy.mylio.domain.options.entity.OptionDetail;
import com.ssafy.mylio.domain.options.entity.Options;
import com.ssafy.mylio.domain.options.repository.OptionDetailRepository;
import com.ssafy.mylio.domain.options.repository.OptionsRepository;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.extern.slf4j.Slf4j;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class OptionDetailService {

    private final OptionDetailRepository optionDetailRepository;
    private final StoreRepository storeRepository;
    private final OptionsRepository optionsRepository;

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
        Store store = getStoreId(storeId);
        Options options = optionsRepository.findById(optionId)
                .orElseThrow(()-> new CustomException(ErrorCode.OPTION_NOT_FOUND, "optionId", optionId));

        if(!options.getStore().getId().equals(storeId)){
            throw new CustomException(ErrorCode.OPTION_STORE_NOT_MATCH, "optionId", optionId)
                    .addParameter("storeId", storeId);
        }

        OptionDetail optionDetail = optionDetailRequestDto.toEntity(options);
        optionDetailRepository.save(optionDetail);
    }

    @Transactional
    public void updateOptionDetail(Integer storeId, Integer optionDetailId, OptionDetailUpdateRequestDto optionDetailUpdateDto){
        Store store = getStoreId(storeId);
        OptionDetail optionDetail = optionDetailRepository.findById(optionDetailId)
                .orElseThrow(()-> new CustomException(ErrorCode.OPTION_DETAIL_NOT_FOUND, "optionDetailId", optionDetailId));

        if(!optionDetail.getOptions().getStore().getId().equals(storeId)){
            throw new CustomException(ErrorCode.OPTION_STORE_NOT_MATCH, "optionDetailId", optionDetailId)
                    .addParameter("storeId", storeId);
        }

        optionDetail.update(optionDetailUpdateDto.getValue(), optionDetailUpdateDto.getAdditionalPrice(), optionDetailUpdateDto.getStatus());
    }

    private Store getStoreId(Integer storeId){
        return storeRepository.findById(storeId)
                .orElseThrow(()-> new CustomException(ErrorCode.STORE_NOT_FOUND, "storeId", storeId));
    }
}
