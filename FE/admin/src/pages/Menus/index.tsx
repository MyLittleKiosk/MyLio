import React, { useState } from 'react';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Select from '@/components/common/Select';
import Table from '@/components/common/Table';

import { MENU_NAV_LIST } from '@/datas/menuList';
import CATEGORY_LIST from '@/datas/categoryList';
import STORE_LIST from '@/datas/storeList';

import IconAdd from '@/assets/icons/IconAdd';

import { Category } from '@/types/categories';
import { Store } from '@/types/stores';
import Modal from '@/components/common/Modal';
import useModalStore from '@/stores/useModalStore';
import AddMenuModal from '@/components/menus/AddMenuModal';

const Menus = () => {
  const { openModal } = useModalStore();

  const [selectedNav, setSelectedNav] = useState(MENU_NAV_LIST[0]);
  const [searchValue, setSearchValue] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<Category | null>(
    null
  );
  const [selectedStore, setSelectedStore] = useState<Store | null>(null);

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
    <>
      <section className='w-full h-full p-4 flex flex-col gap-2 '>
        <h1 className='text-2xl font-preBold h-[5%]'>메뉴 목록</h1>
        <nav className='bg-subContent/50 rounded-md p-2 w-fit'>
          <ul className='flex items-center justify-center gap-2 text-sm font-preMedium'>
            {MENU_NAV_LIST.map((navItem, index) => {
              return (
                <li
                  key={index}
                  onClick={() => setSelectedNav(navItem)}
                  className={`cursor-pointer hover:bg-white rounded-md px-2 py-1 ${
                    selectedNav.title === navItem.title && 'bg-white'
                  }`}
                >
                  {navItem.title}
                </li>
              );
            })}
          </ul>
        </nav>
        <div className='flex gap-2 max-h-[10%] w-full justify-between'>
          <Input
            inputId='searchMenu'
            placeholder='메뉴명 또는 설명으로 검색'
            inputType='text'
            inputValue={searchValue}
            onChange={handleSearchChange}
            className='w-[65%]'
          />
          <Select<Category>
            options={CATEGORY_LIST.content}
            selected={selectedCategory}
            onChange={handleCategoryChange}
            placeholder='모든 카테고리'
            className='w-[11%]'
            getOptionLabel={(option) => option.name_kr}
            getOptionValue={(option) => option.name_kr}
          />
          <Select<Store>
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
        <Table
          title='메뉴 목록'
          description='총 6개의 메뉴가 있습니다.'
          columns={selectedNav.columns}
          data={selectedNav.data.content}
        />
      </section>
      <Modal />
    </>
  );
};

export default Menus;
