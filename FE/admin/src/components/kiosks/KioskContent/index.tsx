import React, { useState } from 'react';

import IconAdd from '@/assets/icons/IconAdd';
import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import Table from '@/components/common/Table';
import Modal from '@/components/common/Modal';
import AddKioskModal from '@/components/kiosks/AddKioskModal';
import EditKioskModal from '@/components/kiosks/EditKioskModal';

import { KIOSK_COLUMNS } from '@/datas/kioskList';

import useModalStore from '@/stores/useModalStore';
import { useGetKioskList } from '@/service/queries/kiosk';
import DeleteKioskModal from '@/components/kiosks/DeleteKioskModal';
import PageNavigation from '@/components/common/PageNavigation';
import { Pagination } from '@/types/apiResponse';
import { useDebounce } from '@/hooks/useDebounce';

const KioskContent = () => {
  const { openModal } = useModalStore();

  const [searchParams, setSearchParams] = useState<{
    keyword?: string;
    page?: number;
  }>({
    page: 1,
  });

  const debouncedKeyword = useDebounce(searchParams.keyword, 500);

  const { data: kioskList, pageInfo } = useGetKioskList(
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
      <h1 className='text-2xl font-preBold h-[5%]'>키오스크 목록</h1>
      <div className='flex gap-2 max-h-[10%] w-full justify-between'>
        <Input
          id='searchKiosk'
          placeholder='키오스크명 또는 위치로 검색'
          type='text'
          value={searchParams.keyword}
          onChange={handleSearchChange}
          className='w-[80%]'
        />
        <Button
          type='button'
          text='키오스크 등록'
          icon={<IconAdd fillColor='white' />}
          onClick={() => {
            openModal(<AddKioskModal />);
          }}
          className='max-w-[15%]'
        />
      </div>
      <Table
        title='키오스크 목록'
        description={`총 ${pageInfo.totalElements}개의 키오스크가 있습니다.`}
        columns={KIOSK_COLUMNS}
        data={kioskList}
        onEdit={(row) => {
          openModal(<EditKioskModal row={row} />);
        }}
        onDelete={(row) => {
          openModal(<DeleteKioskModal row={row} />);
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

export default KioskContent;
