import React, { createContext, useContext, useEffect } from 'react';

import { useMenuAdd } from '@/components/menus/AddMenuForm/useMenuAdd';

import { MenuDetailGetType } from '@/types/menus';
import { IngredientDetailGetType, IngredientType } from '@/types/ingredient';
import { CategoryType } from '@/types/categories';

// 기존 useMenuAdd의 반환 타입과 동일한 타입을 사용
const MenuEditContext = createContext<ReturnType<typeof useMenuAdd> | null>(
  null
);

interface MenuEditProviderProps {
  children: React.ReactNode;
  menuDetail?: MenuDetailGetType;
  category: CategoryType[];
  ingredient: IngredientType[];
}

export const MenuEditProvider: React.FC<MenuEditProviderProps> = ({
  children,
  menuDetail,
  category,
  ingredient,
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
        categoryId: 0, //별도처리
        description: menuDetail.menuInfo.description,
        price: menuDetail.menuInfo.price,
        tags: menuDetail.tags.map((tag) => ({
          tagKr: tag.tagKr,
          tagEn: tag.tagEn,
        })),
        nutritionInfo: menuDetail.nutritionInfo.map((nutrition) => ({
          nutritionTemplateId: nutrition.nutritionId,
          nutritionValue: Number(nutrition.nutritionValue),
        })),
        ingredientInfo: menuDetail.ingredientInfo.map(
          (ingredient) => ingredient.ingredientId
        ),
        optionInfo: [], // 옵션 정보는 별도로 처리
      });

      // 카테고리 설정
      const selectedCategoryId = category.find(
        (category) => category.nameKr === menuDetail.menuInfo.category
      );
      if (selectedCategoryId) {
        menuFormValues.setSelectedCategory(selectedCategoryId);
      }

      // 영양성분 설정
      const nutrientList = menuDetail.nutritionInfo.map((nutrition) => {
        return {
          nutritionTemplateId: nutrition.nutritionId,
          nutritionName: nutrition.nutritionName || '',
          nutritionValue: nutrition.nutritionValue,
        };
      });
      menuFormValues.setSelectedNutrientList(nutrientList);

      // 원재료 설정
      const ingredientList = menuDetail.ingredientInfo
        .map((mi: IngredientDetailGetType) => {
          const foundIngredient = ingredient.find(
            (i) => i.ingredientTemplateId === mi.ingredientId
          );
          return foundIngredient as IngredientType;
        })
        .filter(Boolean);
      menuFormValues.setSelectedIngredientList(ingredientList);

      // 영양성분 설정

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
