import { CategoryType } from '@/types/categories';
import { Column } from '@/types/tableProps';

const CATEGORY_COLUMNS: Column<CategoryType>[] = [
  {
    header: '카테고리명',
    accessor: 'nameKr' as keyof CategoryType,
  },
  {
    header: '편집',
    accessor: 'edit' as keyof CategoryType,
  },
  {
    header: '삭제',
    accessor: 'delete' as keyof CategoryType,
  },
];

export { CATEGORY_COLUMNS };
