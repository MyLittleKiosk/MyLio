import IconAdd from '@/assets/icons/IconAdd';

import Button from '@/components/common/Button';
import Table from '@/components/common/Table';
import AddCategoryModal from '@/components/menus/AddCategoryModal';
import EditCategoryModal from '@/components/menus/EditCategoryModal';
import DeleteCategoryModal from '@/components/menus/DeleteCategoryModal';

import { CategoryType } from '@/types/categories';
import { NavItemType } from '@/types/menus';
import { Column } from '@/types/tableProps';

import useModalStore from '@/stores/useModalStore';

import { useGetCategory } from '@/service/queries/category';
import PageNavigation from '@/components/common/PageNavigation';
import { Pagination } from '@/types/apiResponse';
import { useState } from 'react';

const Category = ({ selectedNav }: { selectedNav: NavItemType }) => {
  const { openModal } = useModalStore();

  const [searchParams, setSearchParams] = useState<{
    page?: number;
  }>({
    page: 1,
  });

  const { data: categoryList, pageInfo } = useGetCategory(searchParams.page);

  function handlePageChange(page: number) {
    setSearchParams({
      ...searchParams,
      page,
    });
  }

  return (
    <div className='flex flex-col gap-2'>
      <div className='flex gap-2 max-h-[10%] w-full items-center justify-between'>
        <h3 className='text-lg font-preMedium'>카테고리 관리</h3>
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
        description={`총 ${categoryList.length}개의 카테고리가 있습니다.`}
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
