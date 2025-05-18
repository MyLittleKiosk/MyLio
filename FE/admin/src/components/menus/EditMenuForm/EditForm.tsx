import { useEffect } from 'react';

import Input from '@/components/common/Input';
import Select from '@/components/common/Select';
import Button from '@/components/common/Button';
import EditOptionTable from '@/components/menus/EditMenuForm/EditOptionTable';
import { useMenuEditContext } from '@/components/menus/EditMenuForm/MenuEditContext';

import { useGetCategory } from '@/service/queries/category';
import { useGetOptions } from '@/service/queries/option';
import { useGetIngredientList } from '@/service/queries/ingredient';
import { useGetNutritionList } from '@/service/queries/nutrient';

import IconAdd from '@/assets/icons/IconAdd';
import IconTrashCan from '@/assets/icons/IconTrashCan';
import IconImage from '@/assets/icons/IconImage';

import translator from '@/utils/translator';

const EditForm = () => {
  const {
    menuAddData,
    selectedCategory,
    tagValueKR,
    tagValueEN,
    nutritionValue,
    selectedIngredientList,
    selectedNutrientList,
    selectedIngredient,
    selectedNutrient,
    selectedOptions,
    imagePreview,
    setMenuAddData,
    setTagValueEN,
    handleTagAdd,
    handleTagDelete,
    handleTagInputChange,
    handleCategoryChange,
    handleIngredientChange,
    handleIngredientRemove,
    handleNutrientAdd,
    handleNutrientRemove,
    handleNutrientChange,
    setNutritionValue,
    handleImageChange,
    clearImage,
    updateOptionInfo,
  } = useMenuEditContext();

  const { data: options } = useGetOptions();
  const { data: category } = useGetCategory(undefined, undefined, 50);
  const { data: ingredient } = useGetIngredientList(undefined, undefined, 50);
  const { data: nutrient } = useGetNutritionList(undefined, undefined, 50);

  // 옵션 정보가 변경될 때마다 menuAddData 업데이트
  useEffect(() => {
    updateOptionInfo();
  }, [selectedOptions]);

  async function translateName() {
    const translatedValue = await translator(menuAddData.nameKr);
    setMenuAddData({ ...menuAddData, nameEn: translatedValue });
  }

  async function translateTag() {
    const translatedValue = await translator(tagValueKR);
    setTagValueEN(translatedValue);
  }

  return (
    <div className='flex flex-col gap-4 items-center justify-center w-[60%]'>
      <div className='flex gap-5 items-center w-full'>
        <Input
          id='메뉴명'
          placeholder='아이스아메리카노'
          type='text'
          label='메뉴명'
          value={menuAddData.nameKr}
          onChange={(e) =>
            setMenuAddData({ ...menuAddData, nameKr: e.target.value })
          }
          className='w-[40%]'
        />
        <Button
          type='button'
          text='번역하기'
          onClick={() => {
            translateName();
          }}
          className='w-[17%]'
        />
        <Input
          id='메뉴영문명'
          placeholder='Ice Americano'
          type='text'
          label='메뉴 영문명'
          value={menuAddData.nameEn}
          onChange={(e) =>
            setMenuAddData({ ...menuAddData, nameEn: e.target.value })
          }
          className='w-[40%]'
        />
      </div>

      <Select
        options={category || []}
        label='카테고리'
        selected={selectedCategory}
        onChange={(e) => handleCategoryChange(e, category || [])}
        placeholder='카테고리를 선택하세요.'
        getOptionLabel={(option) => option.nameKr}
        getOptionValue={(option) => option.categoryId.toString()}
        className='w-full'
      />

      <Input
        id='가격'
        placeholder='1000'
        type='number'
        min={0}
        max={1000000}
        label='가격'
        value={menuAddData.price}
        onChange={(e) =>
          setMenuAddData({ ...menuAddData, price: Number(e.target.value) })
        }
        className='w-full'
      />

      <Input
        id='설명'
        placeholder='아이스아메리카노 추가 설명'
        type='text'
        label='설명'
        value={menuAddData.description}
        onChange={(e) =>
          setMenuAddData({ ...menuAddData, description: e.target.value })
        }
        className='w-full'
      />

      <div className='flex flex-col gap-2'>
        <div className='flex gap-2'>
          <Input
            id='태그한글명'
            placeholder='달달 혹은 신메뉴'
            type='text'
            label='태그 한글명'
            value={tagValueKR}
            onChange={(e) => handleTagInputChange('KR', e.target.value)}
            className='w-[40%]'
          />
          <Input
            id='태그영문명'
            placeholder='sweet or new menu'
            type='text'
            value={tagValueEN}
            onChange={(e) => handleTagInputChange('EN', e.target.value)}
            className='w-[22%]'
          />

          <Button
            type='button'
            text='번역하기'
            onClick={() => {
              translateTag();
            }}
            className='w-[17%]'
          />

          <Button
            type='button'
            text='추가'
            icon={<IconAdd fillColor='white' />}
            onClick={handleTagAdd}
            className='w-[17%]'
          />
        </div>
        <div className='flex flex-wrap gap-2'>
          {menuAddData.tags &&
            menuAddData.tags.map((data) => {
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
              {imagePreview ? (
                <img
                  src={imagePreview}
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

                    handleImageChange(file);
                  }
                }}
              />
            </div>
            <div className='flex flex-col gap-2'>
              <button
                type='button'
                onClick={() => document.getElementById('imageFile')?.click()}
                className='h-10 px-4 py-2 bg-white border border-subContent rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50'
              >
                이미지 업로드
              </button>
              {imagePreview && (
                <button
                  type='button'
                  onClick={clearImage}
                  className='h-10 px-4 py-2 bg-white border border-subContent rounded-md shadow-sm text-sm font-medium text-red-500 hover:bg-gray-50'
                >
                  이미지 삭제
                </button>
              )}
            </div>
          </div>
          <p className='text-xs text-content font-preMedium'>
            권장 크기: 500×500 픽셀, 최대 2MB
          </p>
        </div>
      </div>

      <div className='flex flex-col gap-2 w-full'>
        <Select
          options={ingredient || []}
          label='원재료'
          selected={selectedIngredient}
          placeholder='원재료를 선택하세요.'
          getOptionLabel={(option) => option.ingredientTemplateName}
          getOptionValue={(option) => option.ingredientTemplateId.toString()}
          onChange={(e) => handleIngredientChange(e, ingredient || [])}
          className='w-full'
        />
        <div className='flex gap-2 w-full'>
          {selectedIngredientList.map((ingredient) => (
            <p
              key={ingredient.ingredientTemplateId}
              className='px-2 py-1 text-sm border border-subContent rounded-full font-preLight cursor-pointer flex gap-1 items-center hover:bg-subContent/50'
              onClick={() => handleIngredientRemove(ingredient)}
            >
              {ingredient.ingredientTemplateName}
              <IconTrashCan width={12} height={12} />
            </p>
          ))}
        </div>
      </div>

      <div className='flex flex-col gap-2 w-full'>
        <div className='flex gap-2'>
          <Select
            options={nutrient || []}
            label='영양성분'
            selected={selectedNutrient}
            placeholder='영양성분을 선택하세요.'
            getOptionLabel={(option) => option.nutritionTemplateName}
            getOptionValue={(option) => option.nutritionTemplateId.toString()}
            onChange={(e) => handleNutrientChange(e, nutrient || [])}
            className='w-[55%]'
          />

          <Input
            id='영양성분값'
            placeholder='12'
            type='number'
            min={0}
            max={1000000}
            value={nutritionValue}
            onChange={(e) => {
              setNutritionValue(Number(e.target.value));
            }}
            className='w-[45%]'
          />

          <Button
            icon={<IconAdd fillColor='white' />}
            type='button'
            onClick={() =>
              handleNutrientAdd(
                selectedNutrient?.nutritionTemplateId.toString() || '',
                nutritionValue
              )
            }
          />
        </div>

        <div className='flex gap-2'>
          {selectedNutrientList.map((nutrient) => {
            return (
              <p
                key={nutrient.nutritionTemplateId}
                className='px-2 py-1 text-sm border border-subContent rounded-full font-preLight cursor-pointer flex gap-1 items-center hover:bg-subContent/50'
                onClick={() =>
                  handleNutrientRemove(nutrient.nutritionTemplateId)
                }
              >
                {nutrient.nutritionName + ' ' + nutrient.nutritionValue}
                <IconTrashCan width={12} height={12} />
              </p>
            );
          })}
        </div>
      </div>

      <div className='w-full'>
        <h2 className='text-md font-preSemiBold min-w-[80px] max-w-[100px]'>
          옵션 그룹
        </h2>
        <EditOptionTable options={options} />
      </div>
    </div>
  );
};

export default EditForm;
