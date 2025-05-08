import React, { useState } from 'react';

import IconAdd from '@/assets/icons/IconAdd';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Select from '@/components/common/Select';
import Table from '@/components/common/Table';
import AddMenuModal from '@/components/menus/AddMenuModal';

import STORE_LIST from '@/datas/storeList';

import { CategoryType } from '@/types/categories';
import { StoreType } from '@/types/stores';
import { MenuType, NavItemType } from '@/types/menus';
import { Column } from '@/types/tableProps';

import useModalStore from '@/stores/useModalStore';

import useGetMenus from '@/service/queries/menu';
import useGetCategory from '@/service/queries/category';

const Menu = ({ selectedNav }: { selectedNav: NavItemType }) => {
  const { openModal } = useModalStore();

  const [searchValue, setSearchValue] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<CategoryType | null>(
    null
  );
  const [selectedStore, setSelectedStore] = useState<StoreType | null>(null);

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setSearchValue(e.target.value);
  }

  function handleCategoryChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const selected = category?.find(
      (category) => category.nameKr === e.target.value
    );
    setSelectedCategory(selected || null);
  }

  function handleStoreChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const selected = STORE_LIST.find(
      (store) => store.storeName === e.target.value
    );
    setSelectedStore(selected || null);
  }

  const { data: menus, isLoading: getMenusLoading } = useGetMenus();
  const { data: category, isLoading: getCategoryLoading } = useGetCategory();

  if (!menus || !category || getMenusLoading || getCategoryLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className='flex flex-col gap-2'>
      <div className='flex gap-2 max-h-[10%] w-full justify-between'>
        <Input
          inputId='searchMenu'
          placeholder='메뉴명 또는 설명으로 검색'
          inputType='text'
          inputValue={searchValue}
          onChange={handleSearchChange}
          className='w-[65%]'
        />
        <Select<CategoryType>
          options={category}
          selected={selectedCategory}
          onChange={handleCategoryChange}
          placeholder='모든 카테고리'
          className='w-[11%]'
          getOptionLabel={(option) => option.nameKr}
          getOptionValue={(option) => option.nameKr}
        />
        <Select<StoreType>
          options={STORE_LIST}
          selected={selectedStore}
          onChange={handleStoreChange}
          placeholder='모든 점포'
          className='w-[11%]'
          getOptionLabel={(option) => option.storeName}
          getOptionValue={(option) => option.storeName}
        />
        <Button
          buttonType='button'
          text='메뉴 추가'
          icon={<IconAdd fillColor='white' />}
          onClick={() => {
            openModal(<AddMenuModal />);
          }}
          className='w-[11%] items-center justify-center'
        />
      </div>
      <Table<MenuType>
        title='메뉴 목록'
        description='총 6개의 메뉴가 있습니다.'
        columns={selectedNav.columns as Column<MenuType>[]}
        data={menus as MenuType[]}
      />
    </div>
  );
};

export default Menu;
