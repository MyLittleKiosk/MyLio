package com.ssafy.mylio.domain.menu.service;

import com.ssafy.mylio.domain.menu.dto.response.MenuDetailResponseDto;
import com.ssafy.mylio.domain.menu.dto.response.MenuListResponseDto;
import com.ssafy.mylio.domain.menu.dto.response.MenuTagMapDto;
import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.menu.entity.MenuStatus;
import com.ssafy.mylio.domain.menu.entity.MenuTagMap;
import com.ssafy.mylio.domain.menu.repository.MenuRepository;
import com.ssafy.mylio.domain.menu.repository.MenuTagMapRepository;
import com.ssafy.mylio.domain.menuIngredient.dto.response.IngredientInfoDto;
import com.ssafy.mylio.domain.menuIngredient.repository.MenuIngredientRepository;
import com.ssafy.mylio.domain.nutrition.dto.response.NutritionInfoDto;
import com.ssafy.mylio.domain.nutrition.repository.NutritionRepository;
import com.ssafy.mylio.domain.options.dto.response.OptionInfoDto;
import com.ssafy.mylio.domain.options.repository.MenuOptionRepository;
import com.ssafy.mylio.global.common.CustomPage;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.data.domain.Pageable;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class MenuService {

    private final MenuRepository menuRepository;
    private final MenuTagMapRepository menuTagMapRepository;
    private final MenuIngredientRepository menuIngredientRepository;
    private final NutritionRepository nutritionRepository;
    private final MenuOptionRepository menuOptionRepository;

    public CustomPage<MenuListResponseDto> getMenuList(Integer storeId, Integer categoryId, Pageable pageable) {
        // 메뉴 리스트 조회
        Page<Menu> menuList = menuRepository.findByStoreIdAndOptionalCategoryId(storeId, categoryId, pageable);

        // 메뉴 리스트에서 아이디 조회
        List<Integer> menuIds = menuList.stream().map(Menu::getId).toList();
        if (menuIds.isEmpty()) {
            return new CustomPage<>(Page.empty(pageable));
        }

        // 메뉴 아이디로 태그 조회
        List<MenuTagMap> menuTagMaps = menuTagMapRepository.findByMenuIdIn(menuIds);

        // 메뉴와 태그 각각 매핑
        Map<Integer, List<String>> menuIdToTags = menuTagMaps.stream()
                .collect(Collectors.groupingBy(
                        tagMap -> tagMap.getMenu().getId(),
                        Collectors.mapping(MenuTagMap::getTagKr, Collectors.toList())
                ));

        return new CustomPage<>(menuList.map(menu -> MenuListResponseDto.of(menu, menuIdToTags.getOrDefault(menu.getId(), Collections.emptyList()))));
    }

    public MenuDetailResponseDto getMenuDetail(Integer storeId, Integer menuId) {

        Menu menu = getMenuId(menuId);

        // 메뉴 아이디로 태그 조회
        List<MenuTagMapDto> tagsDto = menuTagMapRepository.findAllByMenuId(menu.getId())
                .stream()
                .map(MenuTagMapDto::of)
                .toList();


        // 메뉴 아이디로 영양정보 조회
        List<NutritionInfoDto> nutritionDto = nutritionRepository.findAllByMenuId(menu.getId())
                .stream()
                .map(NutritionInfoDto::of)
                .toList();

        // 메뉴 아이디로 원재료 조회
        List<IngredientInfoDto> ingredientInfoDto = menuIngredientRepository.findAllByMenuId(menu.getId())
                .stream()
                .map(IngredientInfoDto::of)
                .toList();

        // 메뉴 아이디로 옵션 조회
        List<OptionInfoDto> optionInfoDto = menuOptionRepository.findAllByMenuId(menu.getId())
                .stream()
                .map(OptionInfoDto::of)
                .toList();

        return MenuDetailResponseDto.of(menu, tagsDto, nutritionDto, ingredientInfoDto, optionInfoDto);
    }

    @Transactional
    public void deleteMenu(Integer storeId, Integer menuId) {
        Menu menu = getMenuId(menuId);
        menu.updateStatus(MenuStatus.DELETED);
    }

    private Menu getMenuId(Integer menuId) {
        // 메뉴 검증
        return menuRepository.findById(menuId)
                .orElseThrow(() -> new CustomException(ErrorCode.MENU_NOT_FOUND, "menuId", menuId));
    }
}
