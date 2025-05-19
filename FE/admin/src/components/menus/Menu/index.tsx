import React, { useState } from 'react';

import Input from '@/components/common/Input';
import Select from '@/components/common/Select';
import Table from '@/components/common/Table';
import PageNavigation from '@/components/common/PageNavigation';
import DeleteMenuModal from '@/components/menus/DeleteMenuModal';

import { CategoryType } from '@/types/categories';
import { MenuType, NavItemType } from '@/types/menus';
import { Column } from '@/types/tableProps';
import { Pagination } from '@/types/apiResponse';

import { useGetCategory } from '@/service/queries/category';
import { useGetMenus } from '@/service/queries/menu';
import useModalStore from '@/stores/useModalStore';
import { useDebounce } from '@/hooks/useDebounce';

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
  const [selectedCategory, setSelectedCategory] = useState<CategoryType | null>(
    null
  );
  const [searchParams, setSearchParams] = useState<{
    keyword?: string;
    page?: number;
  }>({
    page: 1,
  });

  const debounceKeyword = useDebounce(searchParams.keyword, 500);

  const { openModal } = useModalStore();

  const { data: menus, pageInfo } = useGetMenus(
    debounceKeyword,
    searchParams.page,
    selectedCategory?.categoryId
  );
  const { data: category } = useGetCategory();

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setSearchParams({ ...searchParams, keyword: e.target.value });
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
          value={searchParams.keyword}
          onChange={handleSearchChange}
          className='w-[85%]'
        />
        <Select<CategoryType>
          options={category}
          selected={selectedCategory}
          onChange={handleCategoryChange}
          placeholder='모든 카테고리'
          className='w-[15%]'
          getOptionLabel={(option) => option.nameKr}
          getOptionValue={(option) => option.nameKr}
        />
      </div>
      <Table<MenuType>
        title='메뉴 목록'
        description={`총 ${pageInfo.totalElements}개의 메뉴가 있습니다.`}
        columns={selectedNav.columns as Column<MenuType>[]}
        data={menus as MenuType[]}
        onEdit={(row) => handleEdit(row.menuId)}
        onDelete={(row) => openModal(<DeleteMenuModal row={row} />, 'lg')}
      />
      <PageNavigation
        pageInfo={pageInfo as Pagination}
        onChangePage={(page: number) => handlePageChange(page)}
      />
    </div>
  );
};

export default Menu;
