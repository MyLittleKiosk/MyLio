package com.ssafy.mylio.domain.menuIngredient.service;

import com.ssafy.mylio.domain.menuIngredient.dto.response.IngredientTemplateResponseDto;
import com.ssafy.mylio.domain.menuIngredient.entity.IngredientTemplate;
import com.ssafy.mylio.domain.menuIngredient.repository.IngredientTemplateRepository;
import com.ssafy.mylio.global.common.CustomPage;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class IngredientService {

    private final IngredientTemplateRepository ingredientTemplateRepository;

    public CustomPage<IngredientTemplateResponseDto> getIngredientList(String userType, String keyword, Pageable pageable){

        // userType 검증 (관리자인지)
        if(!userType.equals("SUPER")){
            throw new CustomException(ErrorCode.FORBIDDEN_ACCESS, "userType", userType);
        }

        // 모든 원재료 목록 조회
        Page<IngredientTemplate> ingredientList = ingredientTemplateRepository.findAllByKeyword(keyword, pageable);

        return new CustomPage<>(ingredientList.map(IngredientTemplateResponseDto::of));
    }
}
