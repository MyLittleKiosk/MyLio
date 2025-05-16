import React, { createContext, useContext, useEffect } from 'react';

import { useMenuAdd } from '@/components/menus/AddMenuForm/useMenuAdd';

import { MenuDetailGetType } from '@/types/menus';
import { IngredientType } from '@/types/ingredient';

import { CATEGORY_LIST } from '@/service/mock/dummies/category';

import { INGREDIENT_LIST } from '@/datas/IngredientList';

// 기존 useMenuAdd의 반환 타입과 동일한 타입을 사용
const MenuEditContext = createContext<ReturnType<typeof useMenuAdd> | null>(
  null
);

interface MenuEditProviderProps {
  children: React.ReactNode;
  menuDetail?: MenuDetailGetType;
}

export const MenuEditProvider: React.FC<MenuEditProviderProps> = ({
  children,
  menuDetail,
}) => {
  // 기본 useMenuAdd 훅을 사용
  const menuFormValues = useMenuAdd();

  // menuDetail이 있으면 초기값 설정
  useEffect(() => {
    if (menuDetail) {
      // 메뉴 기본 정보 설정
      menuFormValues.setMenuAddData({
        nameKr: menuDetail.menuInfo.nameKr,
        nameEn: menuDetail.menuInfo.nameEn,
        categoryId: menuDetail.menuInfo.categoryId,
        description: menuDetail.menuInfo.description,
        price: menuDetail.menuInfo.price,
        tags: menuDetail.tags.map((tag) => ({
          tagKr: tag.tagKr,
          tagEn: tag.tagEn,
        })),
        nutritionInfo: menuDetail.nutritionInfo.map((nutrition) => ({
          nutritionTemplateId: nutrition.nutritionId,
          nutritionValue: nutrition.nutritionValue,
        })),
        ingredientInfo: menuDetail.ingredientInfo.map(
          (ingredient) => ingredient.ingredientId
        ),
        optionInfo: [], // 옵션 정보는 별도로 처리
      });

      // 카테고리 설정
      const selectedCategory = CATEGORY_LIST.data.content.find(
        (category) => category.categoryId === menuDetail.menuInfo.categoryId
      );
      if (selectedCategory) {
        menuFormValues.setSelectedCategory(selectedCategory);
      }

      // 영양성분 설정
      const nutrientList = menuDetail.nutritionInfo.map((nutrition) => {
        return {
          nutrientTemplateId: nutrition.nutritionId,
          nutrientName: nutrition.nutritionName || '',
          nutrientValue: nutrition.nutritionValue,
        };
      });
      menuFormValues.setSelectedNutrientList(nutrientList);

      // 원재료 설정
      const ingredientList = menuDetail.ingredientInfo
        .map((ingredient) => {
          const foundIngredient = INGREDIENT_LIST.content.find(
            (i) => i.ingredientTemplateId === ingredient.ingredientId
          );
          return foundIngredient as IngredientType;
        })
        .filter(Boolean);
      menuFormValues.setSelectedIngredientList(ingredientList);

      // 이미지 설정 (URL이 있을 경우)
      if (menuDetail.menuInfo.imageUrl) {
        menuFormValues.setImagePreview(menuDetail.menuInfo.imageUrl);
      }

      // Group optionInfo by optionId
      const optionMap: Record<
        number,
        { isRequired: boolean; selectedDetails: number[] }
      > = {};

      menuDetail.optionInfo.forEach((option) => {
        if (!optionMap[option.menuOptionId]) {
          optionMap[option.menuOptionId] = {
            isRequired: option.required,
            selectedDetails: [],
          };
        }
        optionMap[option.menuOptionId].selectedDetails.push(option.optionId);
      });

      const optionList = Object.entries(optionMap).map(([optionId, value]) => ({
        optionId: Number(optionId),
        isSelected: true,
        isRequired: value.isRequired,
        selectedDetails: value.selectedDetails,
      }));

      menuFormValues.setSelectedOptions(optionList);
    }
  }, [menuDetail]);

  return (
    <MenuEditContext.Provider value={menuFormValues}>
      {children}
    </MenuEditContext.Provider>
  );
};

export const useMenuEditContext = () => {
  const context = useContext(MenuEditContext);
  if (!context) {
    throw new Error(
      'useMenuEditContext must be used within a MenuEditProvider'
    );
  }
  return context;
};
