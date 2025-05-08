import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Select from '@/components/common/Select';
import { useMenuAdd } from '@/components/menus/AddMenuModal/useMenuAdd';

import IconAdd from '@/assets/icons/IconAdd';

import { CATEGORY_LIST } from '@/datas/categoryList';

import IconTrashCan from '@/assets/icons/IconTrashCan';
import IconImage from '@/assets/icons/IconImage';

/**
 * 메뉴 추가 페이지 1단계 컴포넌트
 * 메뉴명, 카테고리, 가격, 설명, 태그, 이미지 입력 폼
 *
 * @returns 메뉴명, 카테고리, 가격, 설명, 태그, 이미지 입력 폼 컴포넌트
 */

const StepOne = () => {
  const {
    menuAddData,
    selectedCategory,
    tagValueKR,
    setMenuAddData,
    handleTagAdd,
    handleTagDelete,
    handleCategoryChange,
    handleTagInputChange,
  } = useMenuAdd();

  return (
    <div className='flex flex-col gap-4'>
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

      <Select
        options={CATEGORY_LIST.content}
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
    </div>
  );
};

export default StepOne;
