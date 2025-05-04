import IconAdd from '@/assets/icons/IconAdd';
import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Select from '@/components/common/Select';
import Table from '@/components/common/Table';
import { KIOSK_COLUMNS, KIOSK_LIST } from '@/datas/kioskList';
import Modal from '@/components/common/Modal';
import useModalStore from '@/stores/useModalStore';
import React, { useState } from 'react';

const Kiosk = () => {
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
    <section className='w-full h-full p-4 flex flex-col gap-2 '>
      <h1 className='text-2xl font-preBold h-[5%]'>키오스크 목록</h1>
      <div className='flex gap-2 max-h-[10%] w-full justify-between'>
        <Input
          inputId='searchKiosk'
          placeholder='키오스크명 또는 위치로 검색'
          inputType='text'
          inputValue={searchValue}
          onChange={handleSearchChange}
          className='w-[65%]'
        />
        <Select
          options={['a', 'b', 'c']}
          selected={selected}
          onChange={handleSelectChange}
          placeholder='모든 키오스크'
          className='w-[11%]'
          getOptionLabel={(option) => option}
          getOptionValue={(option) => option}
        />
        <Button
          buttonType='button'
          text='키오스크 추가'
          icon={<IconAdd fillColor='white' />}
          onClick={() => {
            openModal(<div>open</div>);
          }}
          className='w-[11%] items-center justify-center'
        />
      </div>
      <Table
        title='키오스크 목록'
        description='총 6개의 키오스크가 있습니다.'
        columns={KIOSK_COLUMNS}
        data={KIOSK_LIST.content}
      />
      <Modal />
    </section>
  );
};

export default Kiosk;
