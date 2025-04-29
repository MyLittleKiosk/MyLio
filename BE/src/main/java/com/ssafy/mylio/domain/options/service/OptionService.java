package com.ssafy.mylio.domain.options.service;

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

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
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

    public OptionResponseDto getOptionDetail(Integer storeId, Integer optionId){
        return null;
    }

}
