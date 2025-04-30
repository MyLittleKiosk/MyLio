package com.ssafy.mylio.domain.category.service;

import com.ssafy.mylio.domain.category.dto.response.CategoryListResponseDto;
import com.ssafy.mylio.domain.category.repository.CategoryRepository;
import com.ssafy.mylio.global.common.CustomPage;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class CategoryService {

    private final CategoryRepository categoryRepository;

    public CustomPage<CategoryListResponseDto> getCategoryList(Integer storeId, Pageable pageable){
        // store 검증

        // 카테고리 조회

        return null;
    }
}
