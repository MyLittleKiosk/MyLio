import React, { useState } from 'react';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Select from '@/components/common/Select';

import MENU_LIST from '@/datas/menuList';
import CATEGORY_LIST from '@/datas/categoryList';
import STORE_LIST from '@/datas/storeList';

import IconEdit from '@/assets/icons/IconEdit';
import IconAdd from '@/assets/icons/IconAdd';
import IconTrashCan from '@/assets/icons/IconTrashCan';

const TABLE_HEAD_CLASSNAME =
  'px-4 py-3 text-left text-sm font-preLight text-content';

const Menus = () => {
  const [searchValue, setSearchValue] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedStore, setSelectedStore] = useState('');

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setSearchValue(e.target.value);
  }

  function handleCategoryChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setSelectedCategory(e.target.value);
  }

  function handleStoreChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setSelectedStore(e.target.value);
  }

  return (
    <section className='w-full h-full p-4 flex flex-col gap-2 '>
      <h1 className='text-2xl font-preBold h-[5%]'>메뉴 관리</h1>
      <nav className='bg-subContent/50 rounded-md p-2 w-fit'>
        <ul className='flex items-center justify-center gap-2 text-sm font-preMedium'>
          <li className='cursor-pointer hover:bg-white rounded-md px-2 py-1'>
            메뉴
          </li>
          <li className='cursor-pointer hover:bg-white rounded-md px-2 py-1'>
            카테고리
          </li>
          <li className='cursor-pointer hover:bg-white rounded-md px-2 py-1'>
            태그
          </li>
          <li className='cursor-pointer hover:bg-white rounded-md px-2 py-1'>
            옵션
          </li>
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
        <Select<(typeof CATEGORY_LIST.data.content)[0]>
          options={CATEGORY_LIST.data.content}
          selected={selectedCategory}
          onChange={handleCategoryChange}
          placeholder='모든 카테고리'
          className='w-[11%]'
          getOptionLabel={(option) => option.name_kr}
        />
        <Select<(typeof STORE_LIST.data.stores)[0]>
          options={STORE_LIST.data.stores}
          selected={selectedStore}
          onChange={handleStoreChange}
          placeholder='모든 점포'
          className='w-[11%]'
          getOptionLabel={(option) => option.store_name}
        />
        <Button
          buttonType='button'
          text='메뉴 추가'
          icon={<IconAdd fillColor='white' />}
          className='w-[11%] items-center justify-center'
        />
      </div>
      <article className='w-full flex flex-col gap-2 border border-subContent rounded-md p-4'>
        <h2 className='text-xl font-preBold'>메뉴 목록</h2>
        <p className='text-sm font-preRegular'>총 6개의 메뉴가 있습니다.</p>
        <div className='overflow-x-auto'>
          <table className='w-full border-collapse'>
            <thead className='border-b border-subContent'>
              <tr>
                <th className={TABLE_HEAD_CLASSNAME}>이미지</th>
                <th className={TABLE_HEAD_CLASSNAME}>메뉴명</th>
                <th className={TABLE_HEAD_CLASSNAME}>카테고리</th>
                <th className={TABLE_HEAD_CLASSNAME}>가격</th>
                <th className={TABLE_HEAD_CLASSNAME}>점포</th>
                <th className={TABLE_HEAD_CLASSNAME}>태그</th>
                <th className={TABLE_HEAD_CLASSNAME}>설명</th>
                <th className={TABLE_HEAD_CLASSNAME}>편집</th>
                <th className={TABLE_HEAD_CLASSNAME}>삭제</th>
              </tr>
            </thead>
            <tbody className='divide-y divide-gray-200'>
              {MENU_LIST.data.content.map((menu) => (
                <tr key={menu.menu_id} className='hover:bg-gray-50'>
                  <td className='px-4 py-3'>
                    <img
                      src={menu.image_url}
                      alt='메뉴 이미지'
                      className='w-10 h-10 rounded-md object-cover'
                    />
                  </td>
                  <td className='px-4 py-3 text-sm font-preRegular'>
                    {menu.name_kr}
                  </td>
                  <td className='px-4 py-3 text-sm font-preRegular'>
                    {menu.category}
                  </td>
                  <td className='px-4 py-3 text-sm font-preRegular'>
                    ₩{menu.price.toLocaleString()}
                  </td>
                  <td className='px-4 py-3 text-sm font-preRegular'>
                    {menu.store_name}
                  </td>
                  <td className='px-4 py-3 text-sm font-preRegular'>
                    {menu.tags}
                  </td>
                  <td className='px-4 py-3 text-sm font-preRegular max-w-xs truncate'>
                    {menu.description}
                  </td>
                  <td className='px-4 py-3'>
                    <button className='p-1 hover:bg-gray-100 rounded-md'>
                      <IconEdit />
                    </button>
                  </td>
                  <td className='px-4 py-3'>
                    <button className='p-1 hover:bg-gray-100 rounded-md'>
                      <IconTrashCan fillColor='#D44848' />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </article>
    </section>
  );
};

export default Menus;
