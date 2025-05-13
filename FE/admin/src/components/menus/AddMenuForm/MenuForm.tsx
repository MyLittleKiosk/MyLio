import { useState } from 'react';

import { useMenuAdd } from '@/components/menus/AddMenuForm/useMenuAdd';
import Input from '@/components/common/Input';
import Select from '@/components/common/Select';
import Button from '@/components/common/Button';
import OptionTable from '@/components/menus/AddMenuForm/OptionTable';

import { CATEGORY_LIST } from '@/service/mock/dummies/category';
import { useGetOptions } from '@/service/queries/option';

import IconAdd from '@/assets/icons/IconAdd';
import IconTrashCan from '@/assets/icons/IconTrashCan';
import IconImage from '@/assets/icons/IconImage';

import NUTRIENT_LIST from '@/datas/NutrientList';
import INGREDIENT_LIST from '@/datas/IngredientList';
import translator from '@/utils/translator';

const MenuForm = () => {
  const {
    menuAddData,
    selectedCategory,
    tagValueKR,
    nutritionValue,
    selectedIngredientList,
    selectedNutrientList,
    selectedIngredient,
    selectedNutrient,
    setMenuAddData,
    handleTagAdd,
    handleTagDelete,
    handleCategoryChange,
    handleTagInputChange,
    handleIngredientRemove,
    handleNutrientAdd,
    handleNutrientRemove,
    handleIngredientChange,
    handleNutrientChange,
    setNutritionValue,
  } = useMenuAdd();

  const { data: options, isLoading } = useGetOptions();

  const [selectedOptions, setSelectedOptions] = useState<
    {
      optionId: number;
      isSelected: boolean;
      isRequired: boolean;
      selectedDetails: number[];
    }[]
  >([]);

  async function translateName() {
    const translatedValue = await translator(menuAddData.nameKr);
    setMenuAddData({ ...menuAddData, nameEn: translatedValue });
  }

  const handleOptionSelect = (optionId: number) => {
    setSelectedOptions((prev) => {
      const exists = prev.find((option) => option.optionId === optionId);
      if (exists) {
        return prev.map((option) =>
          option.optionId === optionId
            ? { ...option, isSelected: !option.isSelected }
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
  };

  const handleDetailSelect = (optionId: number, detailId: number) => {
    setSelectedOptions((prev) => {
      const option = prev.find((opt) => opt.optionId === optionId);
      if (!option) return prev;

      return prev.map((opt) =>
        opt.optionId === optionId
          ? {
              ...opt,
              selectedDetails: opt.selectedDetails.includes(detailId)
                ? opt.selectedDetails.filter((id) => id !== detailId)
                : [...opt.selectedDetails, detailId],
            }
          : opt
      );
    });
  };

  const handleRequiredSelect = (optionId: number) => {
    setSelectedOptions((prev) => {
      const exists = prev.find((option) => option.optionId === optionId);
      if (exists) {
        return prev.map((option) =>
          option.optionId === optionId
            ? { ...option, isRequired: !option.isRequired }
            : option
        );
      }
      return prev;
    });
  };

  if (!options || isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className='flex flex-col gap-4'>
      <div className='flex gap-5 items-center'>
        <Input
          inputId='메뉴명'
          placeholder='아이스아메리카노'
          inputType='text'
          label='메뉴명'
          inputValue={menuAddData.nameKr}
          onChange={(e) =>
            setMenuAddData({ ...menuAddData, nameKr: e.target.value })
          }
        />
        <Button
          buttonType='button'
          text='번역하기'
          onClick={() => {
            translateName();
          }}
        />
        <Input
          inputId='메뉴영문명'
          placeholder='Ice Americano'
          inputType='text'
          label='메뉴 영문명'
          inputValue={menuAddData.nameEn}
          onChange={(e) =>
            setMenuAddData({ ...menuAddData, nameEn: e.target.value })
          }
        />
      </div>

      <Select
        options={CATEGORY_LIST.data.content}
        label='카테고리'
        selected={selectedCategory}
        onChange={handleCategoryChange}
        placeholder='카테고리를 선택하세요.'
        getOptionLabel={(option) => option.nameKr}
        getOptionValue={(option) => option.categoryId.toString()}
      />

      <Input
        inputId='가격'
        placeholder='1000'
        inputType='number'
        label='가격'
        inputValue={menuAddData.price}
        onChange={(e) =>
          setMenuAddData({ ...menuAddData, price: Number(e.target.value) })
        }
      />

      <Input
        inputId='설명'
        placeholder='아이스아메리카노 추가 설명'
        inputType='text'
        label='설명'
        inputValue={menuAddData.description}
        onChange={(e) =>
          setMenuAddData({ ...menuAddData, description: e.target.value })
        }
      />

      <div className='flex flex-col gap-2'>
        <div className='flex gap-2'>
          <Input
            inputId='태그'
            placeholder='달달 혹은 신메뉴'
            inputType='text'
            label='태그'
            inputValue={tagValueKR}
            onChange={(e) => handleTagInputChange('KR', e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleTagAdd();
              }
            }}
          />
          <Button
            buttonType='button'
            text='추가'
            icon={<IconAdd fillColor='white' />}
            onClick={handleTagAdd}
          />
        </div>
        <div className='flex flex-wrap gap-2'>
          {menuAddData.tags.map((data) => {
            return (
              <div
                key={data.tagKr}
                className='flex gap-1 text-sm font-preRegular items-center px-2 py-1 border border-subContent rounded-full cursor-pointer hover:bg-subContent/50'
                onClick={() => handleTagDelete(data.tagKr)}
              >
                {data.tagKr}
                <IconTrashCan width={12} height={12} />
              </div>
            );
          })}
        </div>
      </div>

      <div className='flex gap-4 w-full'>
        <label
          htmlFor='imageFile'
          className='min-w-[80px] max-w-[100px] text-md font-preSemiBold whitespace-nowrap'
        >
          이미지
        </label>
        <div className='flex flex-col gap-2 font-preRegular'>
          <div className='flex gap-2 items-center'>
            <div className='flex flex-col items-center justify-center w-32 h-32 border-2 border-dashed border-content2 rounded-lg bg-gray-50 hover:bg-subContent/50 transition-colors'>
              {menuAddData.imageUrl ? (
                <img
                  src={menuAddData.imageUrl}
                  alt='메뉴 이미지'
                  className='w-full h-full object-contain'
                />
              ) : (
                <div className='flex flex-col items-center justify-center p-6'>
                  <IconImage />
                </div>
              )}

              <input
                type='file'
                id='imageFile'
                className='hidden'
                accept='image/*'
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) {
                    // 파일 크기 체크 (2MB = 2 * 1024 * 1024 bytes)
                    const maxSize = 2 * 1024 * 1024; // 2MB in bytes
                    if (file.size > maxSize) {
                      alert('이미지 크기는 2MB 이하여야 합니다.');
                      e.target.value = ''; // 파일 선택 초기화
                      return;
                    }

                    const reader = new FileReader();
                    reader.onload = (e) => {
                      setMenuAddData({
                        ...menuAddData,
                        imageUrl: e.target?.result as string,
                      });
                    };
                    reader.readAsDataURL(file);
                  }
                }}
              />
            </div>
            <button
              type='button'
              onClick={() => document.getElementById('imageFile')?.click()}
              className='h-10 mt-2 px-4 py-2 bg-white border border-subContent rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50'
            >
              이미지 업로드
            </button>
          </div>
          <p className='text-xs text-content font-preMedium'>
            권장 크기: 500×500 픽셀, 최대 2MB
          </p>
        </div>
      </div>

      <div className='flex flex-col gap-2'>
        <Select
          options={INGREDIENT_LIST.content}
          label='원재료'
          selected={selectedIngredient}
          placeholder='원재료를 선택하세요.'
          getOptionLabel={(option) => option.nameKr}
          getOptionValue={(option) => option.ingredientId.toString()}
          onChange={handleIngredientChange}
        />
        <div className='flex gap-2'>
          {selectedIngredientList.map((ingredient) => (
            <p
              key={ingredient}
              className='px-2 py-1 text-sm border border-subContent rounded-full font-preLight'
              onClick={() => handleIngredientRemove(ingredient)}
            >
              {ingredient}
            </p>
          ))}
        </div>
      </div>

      <div className='flex flex-col gap-2'>
        <div className='flex gap-2'>
          <Select
            options={NUTRIENT_LIST.content}
            label='영양성분'
            selected={selectedNutrient}
            placeholder='영양성분을 선택하세요.'
            getOptionLabel={(option) => option.nameKr}
            getOptionValue={(option) => option.nutrientTemplateId.toString()}
            onChange={handleNutrientChange}
            className='w-[55%]'
          />

          <Input
            inputId='영양성분값'
            placeholder='12'
            inputType='number'
            inputValue={nutritionValue}
            onChange={(e) => {
              setNutritionValue(Number(e.target.value));
            }}
            className='w-[45%]'
          />

          <Button
            icon={<IconAdd fillColor='white' />}
            buttonType='button'
            onClick={() =>
              handleNutrientAdd(
                selectedNutrient?.nutrientTemplateId.toString() || '',
                nutritionValue
              )
            }
          />
        </div>

        <div className='flex gap-2'>
          {selectedNutrientList.map((nutrient) => {
            return (
              <p
                key={nutrient.nutrientTemplateId}
                className='px-2 py-1 text-sm border border-subContent rounded-full font-preLight'
                onClick={() =>
                  handleNutrientRemove(nutrient.nutrientTemplateId)
                }
              >
                {nutrient.nutrientName + ' ' + nutrient.nutrientValue}
              </p>
            );
          })}
        </div>
      </div>

      <div>
        <h2 className='text-md font-preSemiBold min-w-[80px] max-w-[100px]'>
          옵션 그룹
        </h2>
        <OptionTable
          options={options}
          onOptionSelect={handleOptionSelect}
          onDetailSelect={handleDetailSelect}
          onRequiredSelect={handleRequiredSelect}
          selectedOptions={selectedOptions}
        />
      </div>
    </div>
  );
};

export default MenuForm;
