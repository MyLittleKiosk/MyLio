import React, { useState } from 'react';

import Input from '@/components/common/Input';
import Modal from '@/components/common/Modal';
import Select from '@/components/common/Select';
import Table from '@/components/common/Table';
import ViewDetailOrderModal from '@/components/orders/ViewDetailOrderModal';

import { ORDER_COLUMNS, ORDER_LIST } from '@/datas/orderList';
import useModalStore from '@/stores/useModalStore';

const Orders = () => {
  const { openModal } = useModalStore();

  const [searchValue, setSearchValue] = useState('');
  const [selected, setSelected] = useState('');

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setSearchValue(e.target.value);
  }

  function handleSelectChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setSelected(e.target.value);
  }

  return (
    <>
      <section className='w-full h-full p-4 flex flex-col gap-2 '>
        <h1 className='text-2xl font-preBold h-[5%]'>주문 관리</h1>
        <div className='flex gap-2 max-h-[10%] w-full justify-between'>
          <div className='flex gap-2 w-full'>
            <Input
              inputId='searchOrder'
              placeholder='주문번호로 검색'
              inputType='text'
              inputValue={searchValue}
              onChange={handleSearchChange}
              className='w-[65%]'
            />
            <Select
              options={['MyLio 강남점', 'MyLio 홍대점', 'MyLio 명동점']}
              selected={selected}
              onChange={handleSelectChange}
              placeholder='모든 점포'
              className='w-[11%] h-full'
              getOptionLabel={(option) => option}
              getOptionValue={(option) => option}
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
