import Table from '@/components/common/Table';
import { CategoryList } from '@/types/categories';
import { MenuList, NavItemType } from '@/types/menus';
import { OptionList, OptionType } from '@/types/options';
import { Column } from '@/types/tableProps';

const Option = ({ selectedNav }: { selectedNav: NavItemType }) => {
  const isOptionData = (
    data: MenuList | CategoryList | OptionList
  ): data is OptionList => {
    return 'content' in data && 'options' in data.content;
  };

  return (
    <>
      <Table<OptionType>
        title='옵션 목록'
        description={`총 6개의 옵션이 있습니다.`}
        columns={selectedNav.columns as Column<OptionType>[]}
        data={
          isOptionData(selectedNav.data) ? selectedNav.data.content.options : []
        }
      />
    </>
  );
};

export default Option;
