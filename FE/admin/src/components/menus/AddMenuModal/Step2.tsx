import IconAdd from '@/assets/icons/IconAdd';
import { useState } from 'react';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Select from '@/components/common/Select';

import INGREDIENT_LIST from '@/datas/IngredientList';
import NUTRIENT_LIST from '@/datas/NutrientList';
import OPTION_LIST from '@/datas/optionList';

import { useMenuAdd } from '@/hooks/useMenuAdd';

import OptionTable from './OptionTable';

const Step2 = () => {
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
          getOptionLabel={(option) => option.name_kr}
          getOptionValue={(option) => option.ingredient_id.toString()}
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
            getOptionLabel={(option) => option.name_kr}
            getOptionValue={(option) => option.nutrient_template_id.toString()}
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
                selectedNutrient?.nutrient_template_id.toString() || '',
                nutritionValue
              )
            }
          />
        </div>
        <div className='flex gap-2'>
          {selectedNutrientList.map((nutrient) => {
            return (
              <p
                key={nutrient.nutrient_template_id}
                className='px-2 py-1 text-sm border border-subContent rounded-full font-preLight'
                onClick={() =>
                  handleNutrientRemove(nutrient.nutrient_template_id)
                }
              >
                {nutrient.nutrient_name + ' ' + nutrient.nutrient_value}
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
          options={[OPTION_LIST.data]}
          onOptionSelect={handleOptionSelect}
          onDetailSelect={handleDetailSelect}
          onRequiredSelect={handleRequiredSelect}
          selectedOptions={selectedOptions}
        />
      </div>
    </>
  );
};

export default Step2;
