import React, { useState } from 'react';

import IconAdd from '@/assets/icons/IconAdd';
import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Select from '@/components/common/Select';
import Table from '@/components/common/Table';
import Modal from '@/components/common/Modal';
import AddKioskModal from '@/components/kiosks/AddKioskModal';
import EditKioskModal from '@/components/kiosks/EditKioskModal';
import CompleteModal from '@/components/common/CompleteModal';

import { KIOSK_COLUMNS } from '@/datas/kioskList';

import useModalStore from '@/stores/useModalStore';
import { useDeleteKiosk, useGetKioskList } from '@/service/queries/kiosk';
import { KioskType } from '@/types/kiosk';

const Kiosk = () => {
  const { openModal } = useModalStore();
  const { data: kioskList, isLoading } = useGetKioskList();
  const { mutate: deleteKiosk } = useDeleteKiosk();

  const [searchValue, setSearchValue] = useState('');
  const [selected, setSelected] = useState('');

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setSearchValue(e.target.value);
  }

  function handleSelectChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setSelected(e.target.value);
  }

  function handleDelete(row: KioskType) {
    deleteKiosk(row.kioskId, {
      onSuccess: () => {
        openModal(
          <CompleteModal
            title='삭제 성공'
            description='키오스크 삭제에 성공했습니다.'
            buttonText='확인'
          />
        );
      },
    });
  }

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <section className='w-full h-full p-4 flex flex-col gap-2 '>
      <h1 className='text-2xl font-preBold h-[5%]'>키오스크 목록</h1>
      <div className='flex gap-2 max-h-[10%] w-full justify-between'>
        <div className='flex gap-2 w-full'>
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
            placeholder='전체'
            className='w-[11%] h-full'
            getOptionLabel={(option) => option}
            getOptionValue={(option) => option}
          />
        </div>
        <Button
          buttonType='button'
          text='키오스크 등록'
          icon={<IconAdd fillColor='white' />}
          onClick={() => {
            openModal(<AddKioskModal />);
          }}
          className='w-[11%] items-center justify-center'
        />
      </div>
      <Table
        title='키오스크 목록'
        description={`총 ${kioskList.length}개의 키오스크가 있습니다.`}
        columns={KIOSK_COLUMNS}
        data={kioskList}
        onEdit={(row) => {
          openModal(<EditKioskModal row={row} />);
        }}
        onDelete={(row) => {
          handleDelete(row);
        }}
      />
      <Modal />
    </section>
  );
};

export default Kiosk;
