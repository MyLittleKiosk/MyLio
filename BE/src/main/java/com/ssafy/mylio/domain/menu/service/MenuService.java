package com.ssafy.mylio.domain.menu.service;

import com.ssafy.mylio.domain.category.entity.Category;
import com.ssafy.mylio.domain.category.repository.CategoryRepository;
import com.ssafy.mylio.domain.menu.dto.request.MenuPostRequestDto;
import com.ssafy.mylio.domain.menu.dto.request.TagRequestDto;
import com.ssafy.mylio.domain.menu.dto.response.MenuDetailResponseDto;
import com.ssafy.mylio.domain.menu.dto.response.MenuListResponseDto;
import com.ssafy.mylio.domain.menu.dto.response.MenuTagMapDto;
import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.menu.entity.MenuStatus;
import com.ssafy.mylio.domain.menu.entity.MenuTagMap;
import com.ssafy.mylio.domain.menu.repository.MenuRepository;
import com.ssafy.mylio.domain.menu.repository.MenuTagMapRepository;
import com.ssafy.mylio.domain.menuIngredient.dto.response.IngredientInfoDto;
import com.ssafy.mylio.domain.menuIngredient.entity.IngredientTemplate;
import com.ssafy.mylio.domain.menuIngredient.entity.MenuIngredient;
import com.ssafy.mylio.domain.menuIngredient.repository.IngredientTemplateRepository;
import com.ssafy.mylio.domain.menuIngredient.repository.MenuIngredientRepository;
import com.ssafy.mylio.domain.nutrition.dto.request.NutritionValuePostRequestDto;
import com.ssafy.mylio.domain.nutrition.dto.response.NutritionInfoDto;
import com.ssafy.mylio.domain.nutrition.entity.NutritionTemplate;
import com.ssafy.mylio.domain.nutrition.entity.NutritionValue;
import com.ssafy.mylio.domain.nutrition.repository.NutritionRepository;
import com.ssafy.mylio.domain.nutrition.repository.NutritionTemplateRepository;
import com.ssafy.mylio.domain.options.dto.request.MenuOptionMapRequestDto;
import com.ssafy.mylio.domain.options.dto.response.OptionInfoDto;
import com.ssafy.mylio.domain.options.entity.MenuOptionMap;
import com.ssafy.mylio.domain.options.entity.OptionDetail;
import com.ssafy.mylio.domain.options.entity.Options;
import com.ssafy.mylio.domain.options.repository.MenuOptionRepository;
import com.ssafy.mylio.domain.options.repository.OptionDetailRepository;
import com.ssafy.mylio.domain.options.repository.OptionsRepository;
import com.ssafy.mylio.domain.store.entity.Store;
import com.ssafy.mylio.domain.store.repository.StoreRepository;
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
    private final StoreRepository storeRepository;
    private final CategoryRepository categoryRepository;
    private final NutritionTemplateRepository nutritionTemplateRepository;
    private final IngredientTemplateRepository ingredientTemplateRepository;
    private final OptionDetailRepository optionDetailRepository;
    private final OptionsRepository optionsRepository;


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

        Menu menu = getMenu(menuId);

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
        Menu menu = getMenu(menuId);
        menu.updateStatus(MenuStatus.DELETED);
    }

    @Transactional
    public void addMenu(Integer storeId, MenuPostRequestDto menuPostRequestDto) {
        // Store 조회
        Store store = storeRepository.findById(storeId)
                .orElseThrow(() -> new CustomException(ErrorCode.STORE_NOT_FOUND, "storeId", storeId));

        // 카테고리 조회
        Category category = categoryRepository.findById(menuPostRequestDto.getCategoryId())
                .orElseThrow(() -> new CustomException(ErrorCode.CATEGORY_NOT_FOUND, "categoryId", menuPostRequestDto.getCategoryId())
                        .addParameter("storeId", storeId));

        // 메뉴 등록
        Menu menu = menuPostRequestDto.toEntity(store, category);
        menuRepository.save(menu);

        // Tag 매핑
        if (menuPostRequestDto.getTags() != null) {
            for (TagRequestDto tagRequestDto : menuPostRequestDto.getTags()) {
                MenuTagMap menuTagMap = tagRequestDto.toEntity(menu, store);
                menuTagMapRepository.save(menuTagMap);
            }
        }

        // 영양정보 매핑
        if (menuPostRequestDto.getNutritionInfo() != null) {
            for (NutritionValuePostRequestDto nutritionDto : menuPostRequestDto.getNutritionInfo()) {
                NutritionTemplate nutritionTemplate = nutritionTemplateRepository.findById(nutritionDto.getNutritionTemplateId())
                        .orElseThrow(() -> new CustomException(ErrorCode.NUTRITION_TEMPLATE_NOT_FOUND, "nutritionTemplateId", nutritionDto.getNutritionTemplateId()));
                NutritionValue nutritionValue = nutritionDto.toEntity(store, menu, nutritionTemplate);
                nutritionRepository.save(nutritionValue);
            }
        }

        // 원재료 매핑
        if (menuPostRequestDto.getIngredientInfo() != null) {
            for (Integer ingredientId : menuPostRequestDto.getIngredientInfo()) {
                IngredientTemplate ingredientTemplate = ingredientTemplateRepository.findById(ingredientId)
                        .orElseThrow(() -> new CustomException(ErrorCode.INGREDIENT_TEMPLATE_NOT_FOUND, "ingredientId", ingredientId));
                MenuIngredient menuIngredient = MenuIngredient.builder()
                        .store(store)
                        .menu(menu)
                        .ingredient(ingredientTemplate)
                        .build();

                menuIngredientRepository.save(menuIngredient);
            }
        }

        // 옵션 매핑
        if(menuPostRequestDto.getOptionInfo()!= null){
            for(MenuOptionMapRequestDto optionDto :menuPostRequestDto.getOptionInfo()){
                Options options = optionsRepository.findById(optionDto.getOptionId())
                        .orElseThrow(() -> new CustomException(ErrorCode.OPTION_NOT_FOUND, "optionsId", optionDto.getOptionId()));
                OptionDetail optionDetail = optionDetailRepository.findById(optionDto.getOptionDetailId())
                        .orElseThrow(() -> new CustomException(ErrorCode.OPTION_DETAIL_NOT_FOUND, "optionDetailId", optionDto.getOptionDetailId()));
                MenuOptionMap menuOptionMap = optionDto.toEntity(menu, options, optionDetail);
                menuOptionRepository.save(menuOptionMap);
            }
        }

    }

    private Menu getMenu(Integer menuId) {
        // 메뉴 검증
        return menuRepository.findById(menuId)
                .orElseThrow(() -> new CustomException(ErrorCode.MENU_NOT_FOUND, "menuId", menuId));
    }
}
