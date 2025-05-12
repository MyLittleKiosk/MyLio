import React, { useState } from 'react';

import Input from '@/components/common/Input';
import Modal from '@/components/common/Modal';
import Table from '@/components/common/Table';
import ViewDetailOrderModal from '@/components/orders/ViewDetailOrderModal';

import { ORDER_COLUMNS, ORDER_LIST } from '@/datas/orderList';
import useModalStore from '@/stores/useModalStore';

const Orders = () => {
  const { openModal } = useModalStore();

  const [startSearchValue, setStartSearchValue] = useState('');
  const [endSearchValue, setEndSearchValue] = useState('');

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setStartSearchValue(e.target.value);
  }

  function handleEndSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setEndSearchValue(e.target.value);
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
              onChange={handleSearchChange}
            />
            <Input
              inputId='endSearchOrder'
              placeholder=''
              inputType='date'
              inputValue={endSearchValue}
              onChange={handleEndSearchChange}
            />
          </div>
        </div>
        <Table
          title='주문 목록'
          description='총 5개의 주문이 있습니다.'
          columns={ORDER_COLUMNS}
          data={ORDER_LIST.content}
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
