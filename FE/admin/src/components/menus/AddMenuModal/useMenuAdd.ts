import React, { useState } from 'react';

import { MenuAdd } from '@/types/menus';
import { CategoryType } from '@/types/categories';
import { IngredientType } from '@/types/ingredient';
import { NutrientType } from '@/types/nutrient';

import { CATEGORY_LIST } from '@/service/mock/dummies/category';

import INGREDIENT_LIST from '@/datas/IngredientList';
import NUTRIENT_LIST from '@/datas/NutrientList';

interface UseMenuAddReturn {
  menuAddData: MenuAdd;
  selectedCategory: CategoryType | null;
  tagValueKR: string;
  tagValueEN: string;
  nutritionValue: number;
  selectedIngredientList: string[];
  selectedNutrientList: {
    nutrientTemplateId: number;
    nutrientName: string;
    nutrientValue: number;
  }[];
  selectedIngredient: IngredientType | null;
  selectedNutrient: NutrientType | null;
  setNutritionValue: (value: number) => void;
  handleCategoryChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  handleTagInputChange: (type: 'KR' | 'EN', value: string) => void;
  handleTagAdd: () => void;
  handleTagDelete: (tagKR: string) => void;
  handleIngredientAdd: (ingredientId: string) => void;
  handleIngredientChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  handleIngredientRemove: (ingredient: string) => void;
  handleNutrientAdd: (nutrientId: string, value: number) => void;
  handleNutrientChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  handleNutrientRemove: (nutrientId: number) => void;
  resetForm: () => void;
  setMenuAddData: (data: MenuAdd) => void;
}

const initialMenuData: MenuAdd = {
  imageUrl: '',
  nameKr: '',
  nameEn: '',
  categoryId: 0,
  description: '',
  price: 0,
  tags: [],
  nutritionInfo: [],
  ingredientInfo: [],
  optionInfo: [],
};

export const useMenuAdd = (): UseMenuAddReturn => {
  const [menuAddData, setMenuAddData] = useState<MenuAdd>(initialMenuData);
  const [selectedCategory, setSelectedCategory] = useState<CategoryType | null>(
    null
  );
  const [tagValueKR, setTagValueKR] = useState<string>('');
  const [tagValueEN, setTagValueEN] = useState<string>('');
  const [nutritionValue, setNutritionValue] = useState<number>(0);
  const [selectedIngredientList, setSelectedIngredientList] = useState<
    string[]
  >([]);
  const [selectedNutrientList, setSelectedNutrientList] = useState<
    {
      nutrientTemplateId: number;
      nutrientName: string;
      nutrientValue: number;
    }[]
  >([]);
  const [selectedIngredient, setSelectedIngredient] =
    useState<IngredientType | null>(null);
  const [selectedNutrient, setSelectedNutrient] = useState<NutrientType | null>(
    null
  );

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = CATEGORY_LIST.content.find(
      (category) => category.categoryId.toString() === e.target.value
    );
    setSelectedCategory(selected || null);
    setMenuAddData((prev) => ({
      ...prev,
      categoryId: selected?.categoryId || 0,
    }));
  };

  const handleTagInputChange = (type: 'KR' | 'EN', value: string) => {
    if (type === 'KR') {
      setTagValueKR(value);
    } else {
      setTagValueEN(value);
    }
  };

  function handleIngredientChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const selected = INGREDIENT_LIST.content.find(
      (ingredient) => ingredient.ingredientId.toString() === e.target.value
    );

    if (!selected) {
      alert('원재료를 선택해주세요.');
      return;
    }

    setSelectedIngredient(selected || null);
    handleIngredientAdd(selected?.ingredientId.toString());
  }

  function handleNutrientChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const selected = NUTRIENT_LIST.content.find(
      (nutrient) => nutrient.nutrientTemplateId.toString() === e.target.value
    );

    if (!selected) {
      alert('영양성분을 선택해주세요.');
      return;
    }

    setSelectedNutrient(selected || null);
  }

  const handleTagAdd = () => {
    if (tagValueKR === '') {
      alert('태그명을 정확하게 입력해주세요.');
      return;
    }

    setMenuAddData((prev) => ({
      ...prev,
      tags: [
        ...prev.tags,
        {
          tagKr: tagValueKR,
          tagEn: tagValueEN,
        },
      ],
    }));
    setTagValueKR('');
    setTagValueEN('');
  };

  function handleTagDelete(tagKR: string) {
    setMenuAddData((prev) => ({
      ...prev,
      tags: prev.tags.filter((tag) => tag.tagKr !== tagKR),
    }));
  }

  const handleIngredientAdd = (ingredientId: string) => {
    setMenuAddData((prev) => ({
      ...prev,
      ingredientInfo: [...prev.ingredientInfo, Number(ingredientId)],
    }));
  };

  const handleIngredientRemove = (ingredient: string) => {
    setSelectedIngredientList((prev) =>
      prev.filter((item) => item !== ingredient)
    );
  };

  const handleNutrientAdd = (nutrientId: string, value: number) => {
    if (!nutrientId || !value) {
      alert('영양성분을 정확히 입력해주세요.');
      return;
    }

    const newNutrient = {
      nutritionTemplateId: Number(nutrientId),
      nutritionValue: value,
    };

    setMenuAddData((prev) => ({
      ...prev,
      nutritionInfo: [...prev.nutritionInfo, newNutrient],
    }));

    setSelectedNutrientList((prev) => [
      ...prev,
      {
        nutrientTemplateId: Number(nutrientId),
        nutrientName: selectedNutrient?.nameKr || '',
        nutrientValue: value,
      },
    ]);
  };

  const handleNutrientRemove = (nutrientId: number) => {
    setSelectedNutrientList((prev) =>
      prev.filter((item) => item.nutrientTemplateId !== nutrientId)
    );
  };

  const resetForm = () => {
    setMenuAddData(initialMenuData);
    setSelectedCategory(null);
    setTagValueKR('');
    setTagValueEN('');
    setNutritionValue(0);
    setSelectedIngredientList([]);
    setSelectedNutrientList([]);
  };

  return {
    menuAddData,
    selectedCategory,
    tagValueKR,
    tagValueEN,
    nutritionValue,
    selectedIngredient,
    selectedNutrient,
    selectedIngredientList,
    selectedNutrientList,
    setMenuAddData,
    setNutritionValue,
    handleCategoryChange,
    handleTagInputChange,
    handleTagAdd,
    handleTagDelete,
    handleIngredientChange,
    handleNutrientChange,
    handleIngredientAdd,
    handleIngredientRemove,
    handleNutrientAdd,
    handleNutrientRemove,
    resetForm,
  };
};
