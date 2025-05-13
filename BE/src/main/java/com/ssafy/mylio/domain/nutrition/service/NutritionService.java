package com.ssafy.mylio.domain.nutrition.service;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.menu.repository.MenuRepository;
import com.ssafy.mylio.domain.nutrition.dto.request.NutritionValuePostRequestDto;
import com.ssafy.mylio.domain.nutrition.dto.response.NutritionResponseDto;
import com.ssafy.mylio.domain.nutrition.entity.NutritionValue;
import com.ssafy.mylio.domain.nutrition.repository.NutritionRepository;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class NutritionService {

    private final NutritionRepository nutritionRepository;
    private final MenuRepository menuRepository;
    private final StoreRepository storeRepository;

    public List<NutritionResponseDto> getNutritionInfo(Integer storeId, Integer menuId){
        Menu menu = menuRepository.findById(menuId)
                .orElseThrow(() -> new CustomException(ErrorCode.MENU_NOT_FOUND, "menuId", menuId));

        if(!storeId.equals(menu.getStore().getId())){
            throw new CustomException(ErrorCode.MENU_STORE_NOT_MATCH,"menuId", menuId)
                    .addParameter("storeId", storeId);
        }

        List<NutritionValue> nutritionValues = nutritionRepository.findAllWithTemplateByMenuId(menuId);

        return nutritionValues.stream()
                .map(NutritionResponseDto::of)
                .collect(Collectors.toList());

    }

    public void nutritionInfoAdd(Integer storeId, Integer menuId, NutritionValuePostRequestDto dto){


    }

}
