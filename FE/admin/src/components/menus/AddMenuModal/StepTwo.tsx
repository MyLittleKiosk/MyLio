import IconAdd from '@/assets/icons/IconAdd';
import { useState } from 'react';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Select from '@/components/common/Select';

import INGREDIENT_LIST from '@/datas/IngredientList';
import NUTRIENT_LIST from '@/datas/NutrientList';

import { useMenuAdd } from '@/components/menus/AddMenuModal/useMenuAdd';

import OptionTable from '@/components/menus/AddMenuModal/OptionTable';
import useGetOptions from '@/service/queries/option';

/**
 * 메뉴 추가 페이지 2단계 컴포넌트
 * 원재료, 영양성분, 옵션 그룹 입력 컴포넌트
 *
 * @returns 원재료, 영양성분, 옵션 그룹 입력 컴포넌트
 */

const StepTwo = () => {
  const {
    nutritionValue,
    selectedIngredientList,
    selectedNutrientList,
    selectedIngredient,
    selectedNutrient,
    handleIngredientRemove,
    handleNutrientAdd,
    handleNutrientRemove,
    handleIngredientChange,
    handleNutrientChange,
    setNutritionValue,
  } = useMenuAdd();

  const { data: options, isLoading } = useGetOptions();

  if (!options || isLoading) {
    return <div>Loading...</div>;
  }

  const [selectedOptions, setSelectedOptions] = useState<
    {
      optionId: number;
      isSelected: boolean;
      isRequired: boolean;
      selectedDetails: number[];
    }[]
  >([]);

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

  return (
    <>
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
    </>
  );
};

export default StepTwo;
