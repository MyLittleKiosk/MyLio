import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Select from '@/components/common/Select';

import IconAdd from '@/assets/icons/IconAdd';

import CATEGORY_LIST from '@/datas/categoryList';

import { useMenuAdd } from '@/hooks/useMenuAdd';
import IconTrashCan from '@/assets/icons/IconTrashCan';

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
        inputValue={menuAddData.name_kr}
        onChange={(e) =>
          setMenuAddData({ ...menuAddData, name_kr: e.target.value })
        }
      />

      <Select
        options={CATEGORY_LIST.content}
        label='카테고리'
        selected={selectedCategory}
        onChange={handleCategoryChange}
        placeholder='카테고리를 선택하세요.'
        getOptionLabel={(option) => option.name_kr}
        getOptionValue={(option) => option.category_id.toString()}
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
                key={data.tag_kr}
                className='flex gap-1 text-sm font-preRegular items-center px-2 py-1 border border-subContent rounded-full cursor-pointer hover:bg-subContent/50'
                onClick={() => handleTagDelete(data.tag_kr)}
              >
                {data.tag_kr}
                <IconTrashCan width={12} height={12} />
              </div>
            );
          })}
        </div>
      </div>

      <div className='flex gap-2'>
        <Input
          inputId='이미지'
          placeholder='이미지를 업로드하세요.'
          inputType='file'
          label='이미지'
          onChange={(e) => {
            setMenuAddData({ ...menuAddData, image_url: e.target.value });
          }}
          inputValue={menuAddData.image_url}
        />
        <img src={menuAddData.image_url} alt='메뉴 이미지' />
      </div>
    </div>
  );
};

export default StepOne;
