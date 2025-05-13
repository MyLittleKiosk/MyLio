package com.ssafy.mylio.domain.nutrition.service;

import com.ssafy.mylio.domain.nutrition.dto.response.NutritionTemplateResponseDto;
import com.ssafy.mylio.domain.nutrition.entity.NutritionTemplate;
import com.ssafy.mylio.domain.nutrition.repository.NutritionTemplateRepository;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
import com.ssafy.mylio.global.common.CustomPage;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class NutritionTemplateService {

    private final StoreRepository storeRepository;
    private final NutritionTemplateRepository nutritionTemplateRepository;

    public CustomPage<NutritionTemplateResponseDto> getNutritionTemplate(String userType, String keyword, Pageable pageable) {
        // 관리자인지 검증
        validateSuperAdmin(userType);

        // 영양성분 템플릿 모두 조회
        Page<NutritionTemplate> nutritionTemplates = nutritionTemplateRepository.findAllByKeyword(keyword, pageable);

        return new CustomPage<>(nutritionTemplates.map(NutritionTemplateResponseDto::of));
    }

    private void validateSuperAdmin(String userType){
        if(!userType.equals("SUPER")){
            throw new CustomException(ErrorCode.FORBIDDEN_ACCESS, "userType", userType);
        }
    }
}
