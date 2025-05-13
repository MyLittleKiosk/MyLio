package com.ssafy.mylio.domain.nutrition.service;

import com.ssafy.mylio.domain.nutrition.repository.NutritionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class NutritionService {

    private final NutritionRepository nutritionRepository;

    public void getNutritionInfo(Integer storeId, Integer menuId){

    }
}
