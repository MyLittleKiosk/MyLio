import React, { useState } from 'react';

import IconAdd from '@/assets/icons/IconAdd';

import AddAccountModal from '@/components/account/AddAccountModal';
import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import Input from '@/components/common/Input';
import Modal from '@/components/common/Modal';
import Table from '@/components/common/Table';
import useModalStore from '@/stores/useModalStore';

import { ACCOUNT_COLUMNS } from '@/datas/Account';
import { useDeleteAccount, useGetAccountList } from '@/service/queries/account';
import { AccountType } from '@/types/account';

const Accounts = () => {
  const { mutate: deleteAccount } = useDeleteAccount();
  const { data: accountList, isLoading } = useGetAccountList();
  const { openModal } = useModalStore();
  const [searchValue, setSearchValue] = useState('');

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    setSearchValue(e.target.value);
  }

  function handleDelete(row: AccountType) {
    deleteAccount({ accountId: row.accountId });
    openModal(
      <CompleteModal
        title='계정 삭제'
        description='계정 삭제가 완료되었습니다.'
        buttonText='확인'
      />
    );
  }

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <section className='w-full h-full p-4 flex flex-col gap-2 '>
        <h1 className='text-2xl font-preBold h-[5%]'>계정 관리</h1>
        <div className='flex gap-2 max-h-[10%] w-full justify-between'>
          <Input
            id='searchMenu'
            placeholder='이름, 이메일, 매장 이름으로 검색'
            type='text'
            value={searchValue}
            onChange={handleSearchChange}
            className='w-[100%]'
          />
          <Button
            type='button'
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
          description={`총 ${accountList?.length}개의 계정이 있습니다.`}
          columns={ACCOUNT_COLUMNS}
          data={accountList || []}
          onDelete={(row) => handleDelete(row)}
        />
      </section>
      <Modal />
    </>
  );
};

export default Accounts;
