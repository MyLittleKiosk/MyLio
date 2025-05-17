import React, { useState } from 'react';

import Input from '@/components/common/Input';
import Select from '@/components/common/Select';
import Table from '@/components/common/Table';
import CompleteModal from '@/components/common/CompleteModal';

import { CategoryType } from '@/types/categories';
import { MenuType, NavItemType } from '@/types/menus';
import { Column } from '@/types/tableProps';

import { useGetCategory } from '@/service/queries/category';
import { useDeleteMenu, useGetMenus } from '@/service/queries/menu';
import useModalStore from '@/stores/useModalStore';
import PageNavigation from '@/components/common/PageNavigation';
import { Pagination } from '@/types/apiResponse';

interface Props {
  selectedNav: NavItemType;
  setIsEditMenuClicked: (value: boolean) => void;
  setClickedMenuId: (value: number) => void;
}

const Menu = ({
  selectedNav,
  setIsEditMenuClicked,
  setClickedMenuId,
}: Props) => {
  const [searchValue, setSearchValue] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<CategoryType | null>(
    null
  );
  const [searchParams, setSearchParams] = useState<{
    page?: number;
  }>({
    page: 1,
  });

  const { openModal } = useModalStore();

  const { data: menus, pageInfo } = useGetMenus(
    searchParams.page,
    selectedCategory?.categoryId
  );
  const { mutate: deleteMenu } = useDeleteMenu();
  const { data: category } = useGetCategory();

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setSearchValue(e.target.value);
  }

  function handleCategoryChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const selected = category?.find(
      (category) => category.nameKr === e.target.value
    );
    setSelectedCategory(selected || null);
  }

  function handleEdit(menuId: number) {
    setIsEditMenuClicked(true);
    setClickedMenuId(menuId);
  }

  function handleDelete(menuId: number) {
    if (!confirm('삭제하시겠습니까?')) {
      return;
    }

    deleteMenu(menuId, {
      onSuccess: () => {
        openModal(
          <CompleteModal
            title='삭제 성공'
            description='메뉴가 삭제되었습니다.'
            buttonText='확인'
          />
        );
      },
    });
  }

  function handlePageChange(page: number) {
    setSearchParams({
      ...searchParams,
      page,
    });
  }

  return (
    <div className='flex flex-col gap-2'>
      <div className='flex gap-2 max-h-[10%] w-full justify-between'>
        <Input
          id='searchMenu'
          placeholder='메뉴명 또는 설명으로 검색'
          value={searchValue}
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
      </div>
      <Table<MenuType>
        title='메뉴 목록'
        description={`총 ${menus.length}개의 메뉴가 있습니다.`}
        columns={selectedNav.columns as Column<MenuType>[]}
        data={menus as MenuType[]}
        onEdit={(row) => handleEdit(row.menuId)}
        onDelete={(row) => handleDelete(row.menuId)}
      />
      <PageNavigation
        pageInfo={pageInfo as Pagination}
        onChangePage={(page: number) => handlePageChange(page)}
      />
    </div>
  );
};

export default Menu;
