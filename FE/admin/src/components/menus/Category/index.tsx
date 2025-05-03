import Table from '@/components/common/Table';
import { CategoryType } from '@/types/categories';
import { NavItemType } from '@/types/menus';
import { Column } from '@/types/tableProps';

const Category = ({ selectedNav }: { selectedNav: NavItemType }) => {
  return (
    <>
      <Table<CategoryType>
        title='카테고리 목록'
        description={`총 6개의 카테고리가 있습니다.`}
        columns={selectedNav.columns as Column<CategoryType>[]}
        data={selectedNav.data.content as CategoryType[]}
      />
    </>
  );
};

export default Category;
