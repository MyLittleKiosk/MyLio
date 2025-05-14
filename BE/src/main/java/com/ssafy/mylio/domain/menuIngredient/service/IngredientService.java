package com.ssafy.mylio.domain.menuIngredient.service;

import com.ssafy.mylio.domain.menuIngredient.dto.request.IngredientTemplateRequestDto;
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
        validateUserType(userType);

        // 모든 원재료 목록 조회
        Page<IngredientTemplate> ingredientList = ingredientTemplateRepository.findAllByKeyword(keyword, pageable);

        return new CustomPage<>(ingredientList.map(IngredientTemplateResponseDto::of));
    }

    @Transactional
    public void ingredientTemplateAdd(String userType, IngredientTemplateRequestDto requestDto){
        // userType 검증 (관리자인지)
        validateUserType(userType);

        // 등록된 원재료가 있는지 조회
        if(ingredientTemplateRepository.existsByNameKr(requestDto.getIngredientTemplateName())){
            throw new CustomException(ErrorCode.INGREDIENT_TEMPLATE_ALREADY_EXISTS, "name", requestDto.getIngredientTemplateName());
        }

        // 등록
        IngredientTemplate ingredientTemplate = requestDto.toEntity();
        ingredientTemplateRepository.save(ingredientTemplate);
    }

    @Transactional
    public void ingredientTemplateUpdate(String userType, Integer ingredientId, IngredientTemplateRequestDto requestDto){
        // userType 검증 (관리자인지)
        validateUserType(userType);

        // 원재료 템플릿 조회
        IngredientTemplate ingredientTemplate = ingredientTemplateRepository.findById(ingredientId)
                .orElseThrow(()-> new CustomException(ErrorCode.INGREDIENT_TEMPLATE_NOT_FOUND, "ingredientId", ingredientId));

        // 업데이트
        ingredientTemplate.update(requestDto.getIngredientTemplateName(), requestDto.getIngredientTemplateNameEn());
    }

    private void validateUserType(String userType){
        if(!userType.equals("SUPER")){
            throw new CustomException(ErrorCode.FORBIDDEN_ACCESS, "userType", userType);
        }
    }
}
