import React, { useState } from 'react';

import IconAdd from '@/assets/icons/IconAdd';

import AddAccountModal from '@/components/account/AddAccountModal';
import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Modal from '@/components/common/Modal';
import Table from '@/components/common/Table';
import useModalStore from '@/stores/useModalStore';

import { ACCOUNT_COLUMNS, DUMMY_ACCOUNT_LIST } from '@/datas/Account';
import { AccountType } from '@/types/account';

const Accounts = () => {
  const { openModal } = useModalStore();
  const [searchValue, setSearchValue] = useState('');

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setSearchValue(e.target.value);
  }

  return (
    <>
      <section className='w-full h-full p-4 flex flex-col gap-2 '>
        <h1 className='text-2xl font-preBold h-[5%]'>계정 관리</h1>
        <div className='flex gap-2 max-h-[10%] w-full justify-between'>
          <Input
            inputId='searchMenu'
            placeholder='이름, 이메일, 매장 이름으로 검색'
            inputType='text'
            inputValue={searchValue}
            onChange={handleSearchChange}
            className='w-[100%]'
          />
          <Button
            buttonType='button'
            text='계정 추가'
            icon={<IconAdd fillColor='white' />}
            onClick={() => {
              openModal(<AddAccountModal />);
            }}
            className='w-[11%] items-center justify-center'
          />
        </div>
        <Table<AccountType>
          title='계정 목록'
          description={`총 ${DUMMY_ACCOUNT_LIST.accounts.length}개의 계정이 있습니다.`}
          columns={ACCOUNT_COLUMNS}
          data={DUMMY_ACCOUNT_LIST.accounts}
        />
      </section>
      <Modal />
    </>
  );
};

export default Accounts;
