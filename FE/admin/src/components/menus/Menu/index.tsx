import React, { useState } from 'react';

import IconAdd from '@/assets/icons/IconAdd';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Select from '@/components/common/Select';
import Table from '@/components/common/Table';

import { CATEGORY_LIST } from '@/datas/categoryList';
import STORE_LIST from '@/datas/storeList';

import { CategoryType } from '@/types/categories';
import { StoreType } from '@/types/stores';

import AddMenuModal from '../AddMenuModal';

import useModalStore from '@/stores/useModalStore';
import { MenuType, NavItemType } from '@/types/menus';
import { Column } from '@/types/tableProps';

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
    const selected = CATEGORY_LIST.content.find(
      (category) => category.name_kr === e.target.value
    );
    setSelectedCategory(selected || null);
  }

  function handleStoreChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const selected = STORE_LIST.stores.find(
      (store) => store.store_name === e.target.value
    );
    setSelectedStore(selected || null);
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
          options={CATEGORY_LIST.content}
          selected={selectedCategory}
          onChange={handleCategoryChange}
          placeholder='모든 카테고리'
          className='w-[11%]'
          getOptionLabel={(option) => option.name_kr}
          getOptionValue={(option) => option.name_kr}
        />
        <Select<StoreType>
          options={STORE_LIST.stores}
          selected={selectedStore}
          onChange={handleStoreChange}
          placeholder='모든 점포'
          className='w-[11%]'
          getOptionLabel={(option) => option.store_name}
          getOptionValue={(option) => option.store_name}
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
        data={selectedNav.data.content as MenuType[]}
      />
    </div>
  );
};

export default Menu;
