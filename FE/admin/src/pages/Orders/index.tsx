import React, { useState } from 'react';

import Input from '@/components/common/Input';
import Modal from '@/components/common/Modal';
import Table from '@/components/common/Table';
import ViewDetailOrderModal from '@/components/orders/ViewDetailOrderModal';
import { useGetOrders } from '@/service/queries/orders';

import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import { ORDER_COLUMNS } from '@/datas/orderList';
import useModalStore from '@/stores/useModalStore';

const Orders = () => {
  const { openModal } = useModalStore();

  const [startSearchValue, setStartSearchValue] = useState('');
  const [endSearchValue, setEndSearchValue] = useState('');
  const [searchParams, setSearchParams] = useState<{
    startDate?: string;
    endDate?: string;
  }>({});

  const { data: ordersData, isLoading } = useGetOrders(
    searchParams.startDate,
    searchParams.endDate
  );

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setStartSearchValue(e.target.value);
  }

  function handleEndSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setEndSearchValue(e.target.value);
  }

  function handleSearch() {
    if (startSearchValue > endSearchValue) {
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
    });
  }

  function handleReset() {
    setStartSearchValue('');
    setEndSearchValue('');
    setSearchParams({});
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
              inputId='startSearchOrder'
              placeholder=''
              inputType='date'
              inputValue={startSearchValue}
              maxDate={endSearchValue}
              onChange={handleSearchChange}
            />
            <Input
              inputId='endSearchOrder'
              placeholder=''
              inputType='date'
              inputValue={endSearchValue}
              minDate={startSearchValue}
              onChange={handleEndSearchChange}
            />
            <Button
              buttonId='searchBtnId'
              buttonType='button'
              text='검색'
              onClick={handleSearch}
            />
            <Button
              buttonId='resetBtnId'
              buttonType='button'
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
          data={ordersData || []}
          onView={(row) => {
            openModal(<ViewDetailOrderModal initialData={row} />);
          }}
        />
        <Modal />
      </section>
    </>
  );
};

export default Orders;
