import Table from '@/components/common/Table';
import { CategoryList } from '@/types/categories';
import { MenuList, NavItemType } from '@/types/menus';
import { OptionDetailType, OptionList } from '@/types/options';
import { Column } from '@/types/tableProps';

const Option = ({ selectedNav }: { selectedNav: NavItemType }) => {
  const isOptionData = (
    data: MenuList | CategoryList | OptionList
  ): data is OptionList => {
    return 'content' in data && 'options' in data.content;
  };

  return (
    <>
      <Table<OptionDetailType>
        title='옵션 목록'
        description={`총 6개의 옵션이 있습니다.`}
        columns={selectedNav.columns as Column<OptionDetailType>[]}
        data={
          isOptionData(selectedNav.data) ? selectedNav.data.content.options : []
        }
      />
    </>
  );
};

export default Option;
