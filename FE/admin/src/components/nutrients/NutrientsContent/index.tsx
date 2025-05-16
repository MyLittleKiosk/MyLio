import React, { useState } from 'react';

import IconAdd from '@/assets/icons/IconAdd';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Modal from '@/components/common/Modal';
import PageNavigation from '@/components/common/PageNavigation';
import Table from '@/components/common/Table';
import AddNutrientModal from '@/components/nutrients/AddNutrientModal';
import EditNutrientModal from '@/components/nutrients/EditNutrientModal';

import { NUTRIENT_COLUMNS } from '@/datas/NutrientList';

import { useDebounce } from '@/hooks/useDebounce';

import useModalStore from '@/stores/useModalStore';

import { Pagination } from '@/types/apiResponse';
import { NutrientType } from '@/types/nutrient';

import { useGetNutritionList } from '@/service/queries/nutrient';

const NutrientsContent = () => {
  const [searchParams, setSearchParams] = useState<{
    keyword?: string;
    page?: number;
  }>({
    page: 1,
  });
  const { openModal } = useModalStore();

  const debouncedKeyword = useDebounce(searchParams.keyword, 500);

  const { data: nutrientList, pageInfo } = useGetNutritionList(
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
      <h1 className='text-2xl font-preBold h-[5%]'>영양성분분 관리</h1>
      <div className='flex gap-2 max-h-[10%] w-full justify-between'>
        <Input
          id='searchNutrition'
          value={searchParams.keyword || ''}
          placeholder='이름, 영문 이름으로 검색'
          onChange={handleSearchChange}
        />
        <Button
          type='button'
          text='영양성분 추가'
          icon={<IconAdd fillColor='white' />}
          onClick={() => {
            openModal(<AddNutrientModal />);
          }}
        />
      </div>
      <Table<NutrientType>
        title='영양성분 목록'
        description={`총 ${pageInfo.totalElements}개의 영양성분이 있습니다.`}
        columns={NUTRIENT_COLUMNS}
        data={nutrientList}
        onEdit={(row) => {
          openModal(<EditNutrientModal row={row} />);
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

export default NutrientsContent;
