import React, { useState } from 'react';
import { MenuAdd } from '@/types/menus';
import { Category } from '@/types/categories';
import { CATEGORY_LIST } from '@/datas/categoryList';
import { Ingredient } from '@/types/ingredient';
import { Nutrient } from '@/types/nutrient';
import INGREDIENT_LIST from '@/datas/IngredientList';
import NUTRIENT_LIST from '@/datas/NutrientList';

interface UseMenuAddReturn {
  menuAddData: MenuAdd;
  selectedCategory: Category | null;
  tagValueKR: string;
  tagValueEN: string;
  nutritionValue: number;
  selectedIngredientList: string[];
  selectedNutrientList: {
    nutrient_template_id: number;
    nutrient_name: string;
    nutrient_value: number;
  }[];
  selectedIngredient: Ingredient | null;
  selectedNutrient: Nutrient | null;
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
  image_url: '',
  name_kr: '',
  name_en: '',
  category_id: 0,
  description: '',
  price: 0,
  tags: [],
  nutrition_info: [],
  ingredient_info: [],
  option_info: [],
};

export const useMenuAdd = (): UseMenuAddReturn => {
  const [menuAddData, setMenuAddData] = useState<MenuAdd>(initialMenuData);
  const [selectedCategory, setSelectedCategory] = useState<Category | null>(
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
      nutrient_template_id: number;
      nutrient_name: string;
      nutrient_value: number;
    }[]
  >([]);
  const [selectedIngredient, setSelectedIngredient] =
    useState<Ingredient | null>(null);
  const [selectedNutrient, setSelectedNutrient] = useState<Nutrient | null>(
    null
  );

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = CATEGORY_LIST.content.find(
      (category) => category.category_id.toString() === e.target.value
    );
    setSelectedCategory(selected || null);
    setMenuAddData((prev) => ({
      ...prev,
      category_id: selected?.category_id || 0,
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
      (ingredient) => ingredient.ingredient_id.toString() === e.target.value
    );

    if (!selected) {
      alert('원재료를 선택해주세요.');
      return;
    }

    setSelectedIngredient(selected || null);
    handleIngredientAdd(selected?.ingredient_id.toString());
  }

  function handleNutrientChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const selected = NUTRIENT_LIST.content.find(
      (nutrient) => nutrient.nutrient_template_id.toString() === e.target.value
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
          tag_kr: tagValueKR,
          tag_en: tagValueEN,
        },
      ],
    }));
    setTagValueKR('');
    setTagValueEN('');
  };

  function handleTagDelete(tagKR: string) {
    setMenuAddData((prev) => ({
      ...prev,
      tags: prev.tags.filter((tag) => tag.tag_kr !== tagKR),
    }));
  }

  const handleIngredientAdd = (ingredientId: string) => {
    setMenuAddData((prev) => ({
      ...prev,
      ingredient_info: [...prev.ingredient_info, Number(ingredientId)],
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
      nutrition_template_id: Number(nutrientId),
      nutrition_value: value,
    };

    setMenuAddData((prev) => ({
      ...prev,
      nutrition_info: [...prev.nutrition_info, newNutrient],
    }));

    setSelectedNutrientList((prev) => [
      ...prev,
      {
        nutrient_template_id: Number(nutrientId),
        nutrient_name: selectedNutrient?.name_kr || '',
        nutrient_value: value,
      },
    ]);
  };

  const handleNutrientRemove = (nutrientId: number) => {
    setSelectedNutrientList((prev) =>
      prev.filter((item) => item.nutrient_template_id !== nutrientId)
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
