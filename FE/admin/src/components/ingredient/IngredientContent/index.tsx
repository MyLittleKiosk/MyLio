import React, { useState } from 'react';

import IconAdd from '@/assets/icons/IconAdd';
import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Modal from '@/components/common/Modal';
import PageNavigation from '@/components/common/PageNavigation';
import Table from '@/components/common/Table';
import AddIngredientModal from '@/components/ingredient/AddIngredientModal';
import EditIngredientModal from '@/components/ingredient/EditIngredientModal';

import { INGREDIENT_COLUMNS } from '@/datas/IngredientList';
import { useDebounce } from '@/hooks/useDebounce';
import { useGetIngredientList } from '@/service/queries/ingredient';
import useModalStore from '@/stores/useModalStore';
import { Pagination } from '@/types/apiResponse';
import { IngredientType } from '@/types/ingredient';

const IngredientContent = () => {
  const [searchParams, setSearchParams] = useState<{
    keyword?: string;
    page?: number;
  }>({
    page: 1,
  });
  const { openModal } = useModalStore();

  const debouncedKeyword = useDebounce(searchParams.keyword, 500);

  const { data: ingredientList, pageInfo } = useGetIngredientList(
    debouncedKeyword,
    searchParams.page
  );

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchParams({ ...searchParams, keyword: e.target.value });
  };

  const handlePageChange = (page: number) => {
    setSearchParams({ ...searchParams, page });
  };

  return (
    <section className='w-full h-full p-4 flex flex-col gap-2 '>
      <h1 className='text-2xl font-preBold h-[5%]'>재료 관리</h1>
      <div className='flex gap-2 max-h-[10%] w-full justify-between'>
        <Input
          id='searchIngredient'
          value={searchParams.keyword || ''}
          placeholder='이름, 영문 이름으로 검색'
          onChange={handleSearchChange}
        />
        <Button
          type='button'
          text='재료 추가'
          icon={<IconAdd fillColor='white' />}
          onClick={() => {
            openModal(<AddIngredientModal />);
          }}
        />
      </div>
      <Table<IngredientType>
        title='재료 목록'
        description={`총 ${pageInfo.totalElements}개의 재료가 있습니다.`}
        columns={INGREDIENT_COLUMNS}
        data={ingredientList || []}
        onEdit={(row) => {
          openModal(<EditIngredientModal row={row} />);
        }}
      />
      <PageNavigation
        pageInfo={pageInfo as Pagination}
        onChangePage={(page: number) => handlePageChange(page)}
      />
      <Modal />
    </section>
  );
};

export default IngredientContent;
