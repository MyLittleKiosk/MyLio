import React, { useState } from 'react';

import Input from '@/components/common/Input';
import Modal from '@/components/common/Modal';
import Table from '@/components/common/Table';
import ViewDetailOrderModal from '@/components/orders/ViewDetailOrderModal';
import { useGetOrders } from '@/service/queries/orders';

import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import PageNavigation from '@/components/common/PageNavigation';
import { ORDER_COLUMNS } from '@/datas/orderList';
import useModalStore from '@/stores/useModalStore';
import { Pagination } from '@/types/apiResponse';
import { OrderType } from '@/types/orders';

const OrderContent = () => {
  const { openModal } = useModalStore();

  const [startSearchValue, setStartSearchValue] = useState('');
  const [endSearchValue, setEndSearchValue] = useState('');
  const [searchParams, setSearchParams] = useState<{
    startDate?: string;
    endDate?: string;
    page?: number;
  }>({
    page: 1,
  });

  const {
    data: ordersData,
    isLoading,
    pageInfo,
  } = useGetOrders(
    searchParams.startDate,
    searchParams.endDate,
    searchParams.page
  );

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setStartSearchValue(e.target.value);
  }

  function handleEndSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setEndSearchValue(e.target.value);
  }

  function handlePageChange(page: number) {
    setSearchParams({
      ...searchParams,
      page,
    });
  }

  function handleSearch() {
    if (endSearchValue && startSearchValue > endSearchValue) {
      openModal(
        <CompleteModal
          title='주문 검색 오류'
          description='시작일이 종료일보다 클 수 없습니다.'
          buttonText='닫기'
        />
      );
      return;
    }
    setSearchParams({
      startDate: startSearchValue || undefined,
      endDate: endSearchValue || undefined,
      page: 1,
    });
  }

  function handleReset() {
    setStartSearchValue('');
    setEndSearchValue('');
    setSearchParams({
      page: 1,
    });
  }

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <section className='w-full h-full p-4 flex flex-col gap-2 '>
        <h1 className='text-2xl font-preBold h-[5%]'>주문 관리</h1>
        <div className='flex gap-2 max-h-[10%] w-full justify-between'>
          <div className='flex gap-2 w-full'>
            <Input
              id='startSearchOrder'
              placeholder=''
              type='date'
              value={startSearchValue}
              maxDate={endSearchValue}
              onChange={handleSearchChange}
            />
            <Input
              id='endSearchOrder'
              placeholder=''
              type='date'
              value={endSearchValue}
              minDate={startSearchValue}
              onChange={handleEndSearchChange}
            />
            <Button
              id='searchBtnId'
              type='button'
              text='검색'
              onClick={handleSearch}
            />
            <Button
              id='resetBtnId'
              type='button'
              text='전체'
              onClick={handleReset}
              className='bg-gray-500 hover:bg-gray-600'
            />
          </div>
        </div>
        <Table
          title='주문 목록'
          description={`총 ${ordersData?.length || 0}개의 주문이 있습니다.`}
          columns={ORDER_COLUMNS}
          data={ordersData as OrderType[]}
          onView={(row) => {
            openModal(<ViewDetailOrderModal initialData={row} />);
          }}
        />
        <PageNavigation
          pageInfo={pageInfo as Pagination}
          onChangePage={(page: number) => handlePageChange(page)}
        />
        <Modal />
      </section>
    </>
  );
};

export default OrderContent;
