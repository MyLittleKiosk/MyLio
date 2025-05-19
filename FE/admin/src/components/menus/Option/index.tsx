import React, { useState } from 'react';
import IconAdd from '@/assets/icons/IconAdd';

import Button from '@/components/common/Button';
import Table from '@/components/common/Table';
import AddOptionGroupModal from '@/components/menus/AddOptionGroupModal';
import EditOptionModal from '@/components/menus/EditOptionModal';
import DeleteOptionModal from '@/components/menus/DeleteOptionModal';
import PageNavigation from '@/components/common/PageNavigation';
import Input from '@/components/common/Input';

import { NavItemType } from '@/types/menus';
import { OptionGroup } from '@/types/options';
import { Column } from '@/types/tableProps';
import { Pagination } from '@/types/apiResponse';

import useModalStore from '@/stores/useModalStore';
import { useGetOptions } from '@/service/queries/option';
import { useDebounce } from '@/hooks/useDebounce';

const Option = ({ selectedNav }: { selectedNav: NavItemType }) => {
  const { openModal } = useModalStore();

  const [searchParams, setSearchParams] = useState<{
    keyword?: string;
    page?: number;
  }>({
    page: 1,
  });

  const debouncedKeyword = useDebounce(searchParams.keyword, 500);

  const { data: options, pageInfo } = useGetOptions(
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
    <div className='flex flex-col gap-2'>
      <div className='flex gap-2 max-h-[10%] w-full items-center justify-between'>
        <Input
          id='searchMenu'
          placeholder='옵션명으로 검색'
          value={searchParams.keyword}
          onChange={handleSearchChange}
          className='w-[85%]'
        />
        <Button
          type='button'
          text='옵션 그룹 추가'
          icon={<IconAdd fillColor='white' />}
          onClick={() => {
            openModal(<AddOptionGroupModal />);
          }}
          className='items-center justify-center'
        />
      </div>
      <Table<OptionGroup>
        title='옵션 목록'
        description={`총 ${pageInfo.totalElements}개의 옵션이 있습니다.`}
        columns={selectedNav.columns as Column<OptionGroup>[]}
        data={options}
        onEdit={(row) => {
          openModal(<EditOptionModal row={row} />, 'lg');
        }}
        onDelete={(row) => {
          openModal(<DeleteOptionModal row={row} />);
        }}
      />
      <PageNavigation
        pageInfo={pageInfo as Pagination}
        onChangePage={(page: number) => handlePageChange(page)}
      />
    </div>
  );
};

export default Option;
