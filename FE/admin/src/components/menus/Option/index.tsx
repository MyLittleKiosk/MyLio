import IconAdd from '@/assets/icons/IconAdd';

import Button from '@/components/common/Button';
import Table from '@/components/common/Table';
import AddOptionGroupModal from '@/components/menus/AddOptionGroupModal';

import { CategoryList } from '@/types/categories';
import { MenuList, NavItemType } from '@/types/menus';
import { OptionList, OptionType } from '@/types/options';
import { Column } from '@/types/tableProps';

import useModalStore from '@/stores/useModalStore';

const Option = ({ selectedNav }: { selectedNav: NavItemType }) => {
  const { openModal } = useModalStore();

  const isOptionData = (
    data: MenuList | CategoryList | OptionList
  ): data is OptionList => {
    return 'content' in data && 'options' in data.content;
  };

  return (
    <div className='flex flex-col gap-2'>
      <div className='flex gap-2 max-h-[10%] w-full items-center justify-between'>
        <h3 className='text-lg font-preMedium'>옵션 관리</h3>
        <Button
          buttonType='button'
          text='옵션그룹 추가'
          icon={<IconAdd fillColor='white' />}
          onClick={() => {
            openModal(<AddOptionGroupModal />);
          }}
          className='items-center justify-center'
        />
      </div>
      <Table<OptionType>
        title='옵션 목록'
        description={`총 6개의 옵션이 있습니다.`}
        columns={selectedNav.columns as Column<OptionType>[]}
        data={
          isOptionData(selectedNav.data) ? selectedNav.data.content.options : []
        }
      />
    </div>
  );
};

export default Option;
