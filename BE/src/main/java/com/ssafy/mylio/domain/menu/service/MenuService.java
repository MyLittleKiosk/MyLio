package com.ssafy.mylio.domain.menu.service;

import com.ssafy.mylio.domain.menu.dto.response.MenuListResponseDto;
import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.menu.repository.MenuRepository;
import com.ssafy.mylio.global.common.CustomPage;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.data.domain.Pageable;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class MenuService {

    private final MenuRepository menuRepository;

    public CustomPage<MenuListResponseDto> getMenuList(Integer storeId, Integer categoryId, Pageable pageable) {
        Page<Menu> menuList = menuRepository.findByStoreIdAndOptionalCategoryId(storeId, categoryId, pageable);
       return new CustomPage<>(null);
    }
}
