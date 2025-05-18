import React, { useState } from 'react';

import IconAdd from '@/assets/icons/IconAdd';

import Button from '@/components/common/Button';
import Table from '@/components/common/Table';
import AddCategoryModal from '@/components/menus/AddCategoryModal';
import EditCategoryModal from '@/components/menus/EditCategoryModal';
import DeleteCategoryModal from '@/components/menus/DeleteCategoryModal';
import PageNavigation from '@/components/common/PageNavigation';
import Input from '@/components/common/Input';

import { CategoryType } from '@/types/categories';
import { NavItemType } from '@/types/menus';
import { Column } from '@/types/tableProps';
import { Pagination } from '@/types/apiResponse';

import useModalStore from '@/stores/useModalStore';

import { useGetCategory } from '@/service/queries/category';
import { useDebounce } from '@/hooks/useDebounce';

const Category = ({ selectedNav }: { selectedNav: NavItemType }) => {
  const { openModal } = useModalStore();

  const [searchParams, setSearchParams] = useState<{
    keyword?: string;
    page?: number;
  }>({
    page: 1,
  });

  const debouncedKeyword = useDebounce(searchParams.keyword, 500);

  const { data: categoryList, pageInfo } = useGetCategory(
    debouncedKeyword,
    searchParams.page
  );

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchParams({ ...searchParams, keyword: e.target.value });
  };

  function handlePageChange(page: number) {
    setSearchParams({
      ...searchParams,
      page,
    });
  }

  return (
    <div className='flex flex-col gap-2'>
      <div className='flex gap-2 max-h-[10%] w-full items-center justify-between'>
        <Input
          id='searchCategory'
          placeholder='카테고리명으로 검색'
          value={searchParams.keyword}
          onChange={handleSearchChange}
          className='w-[85%]'
        />
        <Button
          type='button'
          text='카테고리 추가'
          icon={<IconAdd fillColor='white' />}
          onClick={() => {
            openModal(<AddCategoryModal />);
          }}
          className='items-center justify-center'
        />
      </div>
      <Table<CategoryType>
        title='카테고리 목록'
        description={`총 ${pageInfo.totalElements}개의 카테고리가 있습니다.`}
        columns={selectedNav.columns as Column<CategoryType>[]}
        data={categoryList as CategoryType[]}
        onEdit={(row) => {
          openModal(<EditCategoryModal row={row} />);
        }}
        onDelete={(row) => {
          openModal(<DeleteCategoryModal row={row} />);
        }}
      />
      <PageNavigation
        pageInfo={pageInfo as Pagination}
        onChangePage={(page: number) => handlePageChange(page)}
      />
    </div>
  );
};

export default Category;
