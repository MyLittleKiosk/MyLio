package com.ssafy.mylio.domain.options.service;

import com.ssafy.mylio.domain.options.dto.request.OptionRequestDto;
import com.ssafy.mylio.domain.options.dto.response.OptionDetailDto;
import com.ssafy.mylio.domain.options.dto.response.OptionListResponseDto;
import com.ssafy.mylio.domain.options.dto.response.OptionResponseDto;
import com.ssafy.mylio.domain.options.entity.OptionDetail;
import com.ssafy.mylio.domain.options.entity.Options;
import com.ssafy.mylio.domain.options.repository.OptionDetailRepository;
import com.ssafy.mylio.domain.options.repository.OptionsRepository;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class OptionService {

    private final OptionsRepository optionsRepository;
    private final OptionDetailRepository optionDetailRepository;
    private final StoreRepository storeRepository;

    public OptionListResponseDto getOptionList(Integer storeId){

        Store store = getStoreId(storeId);

        // 1. 매장 아이디로 옵션 모두 조회
        List<Options> optionsList = optionsRepository.findAllByStoreId(store.getId());

        // 2. Options ID 리스트 뽑기
        List<Integer> optionsId = optionsList.stream().map(Options::getId).toList();

        // 3. OptionIds로 OptionDetail 조회
        List<OptionDetail> optionDetails = optionDetailRepository.findAllByOptionsIdIn(optionsId);

        // 4. optionId 기준으로 그룹핑
        Map<Integer, List<OptionDetailDto>> detailMap = optionDetails.stream()
                .collect(Collectors.groupingBy(
                        detail -> detail.getOptions().getId(),
                        Collectors.mapping(OptionDetailDto::of, Collectors.toList())
                ));

        // 5. OptionResponseDto에 담기
        List<OptionResponseDto> optionResponseDtoList = optionsList.stream()
                .map(option -> OptionResponseDto.of(option, detailMap.getOrDefault(option.getId(), List.of())))
                .toList();

        return OptionListResponseDto.of(optionResponseDtoList);
    }

    private Store getStoreId(Integer storeId){
         return storeRepository.findById(storeId)
                .orElseThrow(()-> new CustomException(ErrorCode.STORE_NOT_FOUND, "storeId", storeId));
    }

    private Options getOptionId(Integer optionId){
        return optionsRepository.findById(optionId)
                .orElseThrow(()-> new CustomException(ErrorCode.OPTION_NOT_FOUND, "optionId", optionId));
    }

    public OptionResponseDto getOptionDetail(Integer storeId, Integer optionId){
        // 매장, 옵션 아이디 조회
        Store store = getStoreId(storeId);
        Options options = getOptionId(optionId);

        // 매장의 옵션이 맞는지 조회
        if(!options.getStore().getId().equals(storeId)){
            throw new CustomException(ErrorCode.OPTION_STORE_NOT_MATCH, "optionId", optionId)
                    .addParameter("storeId", storeId);
        }

        // 옵션 Id로 상세옵션 조회
        List<OptionDetail> optionDetails = optionDetailRepository.findAllByOptionsId(options.getId());

        // 상세 옵션 DTO로 변환
        List<OptionDetailDto> optionDetailDto = optionDetails.stream()
                .map(OptionDetailDto::of)
                .toList();

        return OptionResponseDto.of(options, optionDetailDto);
    }

    @Transactional
    public void deleteOption(Integer storeId, Integer optionId){
        // 매장, 옵션 아이디 조회
        Store store = getStoreId(storeId);
        Options options = getOptionId(optionId);

        // 매장의 옵션이 맞는지 조회
        if(!options.getStore().getId().equals(storeId)){
            throw new CustomException(ErrorCode.OPTION_STORE_NOT_MATCH, "optionId", optionId)
                    .addParameter("storeId", storeId);
        }

        // 옵션 STATUS DELETED로 변경
        options.delete();
    }

    @Transactional
    public void addOption(Integer storeId, OptionRequestDto optionRequestDto){
        Store store = getStoreId(storeId);
        Options options = optionRequestDto.toEntity(store);
        optionsRepository.save(options);
    }

}
