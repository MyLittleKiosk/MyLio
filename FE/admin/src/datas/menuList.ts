import { MenuType, NavItemType } from '@/types/menus';
import { Column } from '@/types/tableProps';
import { CATEGORY_COLUMNS } from '@/datas/categoryList';
import { OPTION_COLUMNS } from '@/datas/optionList';

const MENU_COLUMNS: Column<MenuType>[] = [
  {
    header: '이미지',
    accessor: 'imageUrl' as keyof MenuType,
  },
  {
    header: '메뉴명',
    accessor: 'nameKr' as keyof MenuType,
  },
  {
    header: '카테고리',
    accessor: 'category' as keyof MenuType,
  },
  {
    header: '가격',
    accessor: 'price' as keyof MenuType,
  },
  {
    header: '점포',
    accessor: 'storeName' as keyof MenuType,
  },
  {
    header: '설명',
    accessor: 'description' as keyof MenuType,
    className: 'px-4 py-3 text-sm font-preRegular max-w-xs truncate',
  },
  {
    header: '편집',
    accessor: 'edit' as keyof MenuType,
  },
  {
    header: '삭제',
    accessor: 'delete' as keyof MenuType,
  },
];

const MENU_NAV_LIST: NavItemType[] = [
  {
    title: '메뉴',
    columns: MENU_COLUMNS,
  },
  {
    title: '카테고리',
    columns: CATEGORY_COLUMNS,
  },
  {
    title: '옵션',
    columns: OPTION_COLUMNS,
  },
];
export { MENU_COLUMNS, MENU_NAV_LIST };
