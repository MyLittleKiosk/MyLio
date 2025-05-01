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
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class CategoryService {

    private final CategoryRepository categoryRepository;
    private final StoreRepository storeRepository;

    public CustomPage<CategoryResponseDto> getCategoryList(Integer storeId, Pageable pageable){
        // store 검증
        Store store = getStore(storeId);

        // 카테고리 조회
        Page<Category> categoryList = categoryRepository.findAllByStoreId(storeId, pageable);
        return new CustomPage<>(categoryList.map(CategoryResponseDto::of));
    }

    @Transactional
    public void addCategory(Integer storeId, CategoryAddRequestDto categoryAddRequestDto){
        // store 검증
        Store store = getStore(storeId);

        // Entity로 변환
        Category category = categoryAddRequestDto.toEntity(store);
        categoryRepository.save(category);
    }

    @Transactional
    public void updateCategory(Integer storeId, Integer categoryId, CategoryUpdateRequestDto categoryUpdateDto) {
        Category category = getValidCategory(storeId, categoryId); // 카테고리 검증 및 조회
        // 카테고리 업데이트
        category.update(categoryUpdateDto.getNameKr(), categoryUpdateDto.getNameEn(), categoryUpdateDto.getStatus());
    }

    @Transactional
    public void deleteCategory(Integer storeId, Integer categoryId) {
        Category category = getValidCategory(storeId, categoryId); // 카테고리 검증 및 조회
        category.delete(); // 카테고리 삭제
    }

    private Store getStore(Integer storeId){
        return storeRepository.findById(storeId)
                .orElseThrow(()-> new CustomException(ErrorCode.STORE_NOT_FOUND, "storeId", storeId));
    }

    private Category getValidCategory(Integer storeId, Integer categoryId) {
        getStore(storeId);

        // 카테고리 Id 조회
        Category category = categoryRepository.findById(categoryId)
                .orElseThrow(() -> new CustomException(ErrorCode.CATEGORY_NOT_FOUND, "categoryId", categoryId));

        // 매장에 있는 카테고리인지 조회
        if (!category.getStore().getId().equals(storeId)) {
            log.warn("매장에 없는 카테고리입니다, categoryId : {}, storeId : {}", categoryId, storeId);
            throw new CustomException(ErrorCode.CATEGORY_STORE_NOT_MATCH, "categoryId", categoryId)
                    .addParameter("storeId", storeId);
        }

        return category;
    }

}
