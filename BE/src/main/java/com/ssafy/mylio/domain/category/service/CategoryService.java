package com.ssafy.mylio.domain.category.service;

import com.ssafy.mylio.domain.category.dto.request.CategoryAddRequestDto;
import com.ssafy.mylio.domain.category.dto.request.CategoryUpdateRequestDto;
import com.ssafy.mylio.domain.category.dto.response.CategoryResponseDto;
import com.ssafy.mylio.domain.category.entity.Category;
import com.ssafy.mylio.domain.category.repository.CategoryRepository;
import com.ssafy.mylio.domain.store.entity.Store;
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
public class CategoryService {

    private final CategoryRepository categoryRepository;
    private final StoreRepository storeRepository;

    public CustomPage<CategoryResponseDto> getCategoryList(Integer storeId, Pageable pageable){
        // store 검증
        Store store = getStoreId(storeId);

        // 카테고리 조회
        Page<Category> categoryList = categoryRepository.findAllByStoreId(storeId, pageable);
        return new CustomPage<>(categoryList.map(CategoryResponseDto::of));
    }

    @Transactional
    public void addCategory(Integer storeId, CategoryAddRequestDto categoryAddRequestDto){
        // store 검증
        Store store = getStoreId(storeId);

        // Entity로 변환
        Category category = categoryAddRequestDto.toEntity(store);
        categoryRepository.save(category);
    }

    @Transactional
    public void updateCategory(Integer storeId, Integer categoryId, CategoryUpdateRequestDto categoryUpdateDto) {

    }

    private Store getStoreId(Integer storeId){
        return storeRepository.findById(storeId)
                .orElseThrow(()-> new CustomException(ErrorCode.STORE_NOT_FOUND, "storeId", storeId));
    }
}
