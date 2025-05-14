import React, { useState } from 'react';

import { MenuAdd } from '@/types/menus';
import { CategoryType } from '@/types/categories';
import { IngredientType } from '@/types/ingredient';
import { NutrientType } from '@/types/nutrient';
import { OptionInfoType } from '@/types/options';

import { CATEGORY_LIST } from '@/service/mock/dummies/category';

import INGREDIENT_LIST from '@/datas/IngredientList';
import NUTRIENT_LIST from '@/datas/NutrientList';

const initialMenuData: MenuAdd = {
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

export const useMenuAdd = () => {
  const [menuAddData, setMenuAddData] = useState<MenuAdd>(initialMenuData);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const [selectedCategory, setSelectedCategory] = useState<CategoryType | null>(
    null
  );
  const [tagValueKR, setTagValueKR] = useState<string>('');
  const [tagValueEN, setTagValueEN] = useState<string>('');

  const [nutritionValue, setNutritionValue] = useState<number>(0);

  const [selectedIngredient, setSelectedIngredient] =
    useState<IngredientType | null>(null);
  const [selectedIngredientList, setSelectedIngredientList] = useState<
    IngredientType[]
  >([]);

  const [selectedNutrient, setSelectedNutrient] = useState<NutrientType | null>(
    null
  );
  const [selectedNutrientList, setSelectedNutrientList] = useState<
    {
      nutrientTemplateId: number;
      nutrientName: string;
      nutrientValue: number;
    }[]
  >([]);

  const [selectedOptions, setSelectedOptions] = useState<
    {
      optionId: number;
      isSelected: boolean;
      isRequired: boolean;
      selectedDetails: number[];
    }[]
  >([]);

  function handleImageChange(file: File) {
    setImageFile(file);

    // Create preview URL for the image
    const reader = new FileReader();
    reader.onload = (e) => {
      setImagePreview(e.target?.result as string);
    };
    reader.readAsDataURL(file);
  }

  function clearImage() {
    setImageFile(null);
    setImagePreview(null);

    // Reset the file input element
    const fileInput = document.getElementById('imageFile') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
  }

  function handleCategoryChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const selected = CATEGORY_LIST.data.content.find(
      (category) => category.categoryId.toString() === e.target.value
    );
    setSelectedCategory(selected || null);
    setMenuAddData((prev) => ({
      ...prev,
      categoryId: selected?.categoryId || 0,
    }));
  }

  function handleTagInputChange(type: 'KR' | 'EN', value: string) {
    if (type === 'KR') {
      setTagValueKR(value);
    } else {
      setTagValueEN(value);
    }
  }

  function handleTagAdd() {
    if (tagValueKR === '') {
      alert('태그명을 정확하게 입력해주세요.');
      return;
    }

    if (tagValueEN === '') {
      alert('태그영문명을 정확하게 입력해주세요. 번역하기 버튼을 눌러주세요.');
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
  }

  function handleTagDelete(tagKR: string) {
    setMenuAddData((prev) => ({
      ...prev,
      tags: prev.tags.filter((tag) => tag.tagKr !== tagKR),
    }));
  }

  function handleIngredientChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const selected = INGREDIENT_LIST.content.find((ingredient) => {
      return ingredient.ingredientId === Number(e.target.value);
    });

    if (!selected) {
      alert('원재료를 선택해주세요.');
      return;
    }

    // 이미 선택된 원재료인지 확인
    const isDuplicate =
      menuAddData.ingredientInfo.includes(selected.ingredientId) ||
      selectedIngredientList.includes(selected);

    if (isDuplicate) {
      alert('이미 선택된 원재료입니다.');
      return;
    }

    setSelectedIngredient(selected);

    // 원재료 ID 추가
    setMenuAddData((prev) => ({
      ...prev,
      ingredientInfo: [...prev.ingredientInfo, Number(selected.ingredientId)],
    }));

    // 원재료 이름 추가
    setSelectedIngredientList((prev) => [...prev, selected]);
  }

  function handleIngredientRemove(ingredient: IngredientType) {
    setMenuAddData((prev) => ({
      ...prev,
      ingredientInfo: prev.ingredientInfo.filter(
        (item) => item !== ingredient.ingredientId
      ),
    }));

    setSelectedIngredientList((prev) =>
      prev.filter((item) => item.ingredientId !== ingredient.ingredientId)
    );
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

  function handleNutrientAdd(nutrientId: string, value: number) {
    if (!nutrientId || !value) {
      alert('영양성분을 정확히 입력해주세요.');
      return;
    }

    const nutrientTemplateId = Number(nutrientId);

    // 동일한 templateId를 가진 영양성분이 이미 존재하는지 확인
    const isDuplicate =
      menuAddData.nutritionInfo.some(
        (nutrient) => nutrient.nutritionTemplateId === nutrientTemplateId
      ) ||
      selectedNutrientList.some(
        (nutrient) => nutrient.nutrientTemplateId === nutrientTemplateId
      );

    if (isDuplicate) {
      alert('동일한 영양성분이 이미 추가되어 있습니다.');
      return;
    }

    const newNutrient = {
      nutritionTemplateId: nutrientTemplateId,
      nutritionValue: value,
    };

    setMenuAddData((prev) => ({
      ...prev,
      nutritionInfo: [...prev.nutritionInfo, newNutrient],
    }));

    setSelectedNutrientList((prev) => [
      ...prev,
      {
        nutrientTemplateId: nutrientTemplateId,
        nutrientName: selectedNutrient?.nameKr || '',
        nutrientValue: value,
      },
    ]);
  }

  function handleNutrientRemove(nutrientId: number) {
    setMenuAddData((prev) => ({
      ...prev,
      nutritionInfo: prev.nutritionInfo.filter(
        (item) => item.nutritionTemplateId !== nutrientId
      ),
    }));

    setSelectedNutrientList((prev) =>
      prev.filter((item) => item.nutrientTemplateId !== nutrientId)
    );
  }

  function handleOptionSelect(optionId: number) {
    setSelectedOptions((prev) => {
      const exists = prev.find((option) => option.optionId === optionId);
      if (exists) {
        // If we're unselecting the option, clear the selectedDetails
        const newIsSelected = !exists.isSelected;
        return prev.map((option) =>
          option.optionId === optionId
            ? {
                ...option,
                isSelected: newIsSelected,
                // If we're unselecting, clear the selectedDetails
                selectedDetails: newIsSelected ? option.selectedDetails : [],
                // If we're unselecting, also clear isRequired
                isRequired: newIsSelected ? option.isRequired : false,
              }
            : option
        );
      }
      return [
        ...prev,
        {
          optionId,
          isSelected: true,
          isRequired: false,
          selectedDetails: [],
        },
      ];
    });
  }

  function handleDetailSelect(optionId: number, detailId: number) {
    setSelectedOptions((prev) => {
      const option = prev.find((opt) => opt.optionId === optionId);
      if (!option) {
        return [
          ...prev,
          {
            optionId,
            isSelected: true,
            isRequired: false,
            selectedDetails: [detailId],
          },
        ];
      }

      const isAddingDetail = !option.selectedDetails.includes(detailId);

      return prev.map((opt) =>
        opt.optionId === optionId
          ? {
              ...opt,
              isSelected: isAddingDetail ? true : opt.isSelected,
              selectedDetails: opt.selectedDetails.includes(detailId)
                ? opt.selectedDetails.filter((id) => id !== detailId)
                : [...opt.selectedDetails, detailId],
            }
          : opt
      );
    });
  }

  function handleRequiredSelect(optionId: number) {
    setSelectedOptions((prev) => {
      const exists = prev.find((option) => option.optionId === optionId);
      if (exists) {
        return prev.map((option) =>
          option.optionId === optionId
            ? {
                ...option,
                isRequired: !option.isRequired,
                isSelected: !option.isRequired ? true : option.isSelected,
              }
            : option
        );
      }
      return [
        ...prev,
        {
          optionId,
          isSelected: true,
          isRequired: true,
          selectedDetails: [],
        },
      ];
    });
  }

  function updateOptionInfo() {
    const optionInfo: OptionInfoType[] = [];

    selectedOptions.forEach((option) => {
      if (option.isSelected) {
        if (option.selectedDetails.length > 0) {
          option.selectedDetails.forEach((detailId) => {
            optionInfo.push({
              optionId: option.optionId,
              isRequired: option.isRequired,
              optionDetailId: detailId,
            });
          });
        }
      }
    });

    setMenuAddData((prev) => ({
      ...prev,
      optionInfo,
    }));
  }

  function resetForm() {
    setMenuAddData(initialMenuData);
    setSelectedCategory(null);
    setTagValueKR('');
    setTagValueEN('');
    setNutritionValue(0);
    setSelectedIngredientList([]);
    setSelectedNutrientList([]);
    setSelectedOptions([]);
    setImageFile(null);
    setImagePreview(null);
  }

  function checkValidation() {
    if (menuAddData.nameKr === '' || menuAddData.nameEn === '') {
      return false;
    }

    if (menuAddData.description === '') {
      return false;
    }

    if (menuAddData.price === 0) {
      return false;
    }

    if (menuAddData.tags.length === 0) {
      return false;
    }

    if (selectedCategory === null) {
      return false;
    }

    if (selectedIngredientList.length === 0) {
      return false;
    }

    if (selectedNutrientList.length === 0) {
      return false;
    }

    if (selectedOptions.length === 0) {
      return false;
    }

    if (imageFile === null) {
      return false;
    }

    return true;
  }

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
    selectedOptions,
    imageFile,
    imagePreview,
    setMenuAddData,
    setTagValueEN,
    setNutritionValue,
    handleCategoryChange,
    handleTagInputChange,
    handleTagAdd,
    handleTagDelete,
    handleIngredientChange,
    handleNutrientChange,
    handleIngredientRemove,
    handleNutrientAdd,
    handleNutrientRemove,
    handleOptionSelect,
    handleDetailSelect,
    handleRequiredSelect,
    handleImageChange,
    clearImage,
    updateOptionInfo,
    resetForm,
    checkValidation,
  };
};
