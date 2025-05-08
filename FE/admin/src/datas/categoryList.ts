import { PaginationResponse } from '@/types/apiResponse';
import { CategoryType } from '@/types/categories';
import { Column } from '@/types/tableProps';

const CATEGORY_COLUMNS: Column<CategoryType>[] = [
  {
    header: '카테고리명',
    accessor: 'name_kr' as keyof CategoryType,
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

const CATEGORY_LIST: PaginationResponse<CategoryType> = {
  content: [
    {
      categoryId: 1,
      nameKr: '커피',
      nameEn: 'coffee',
    },
    {
      categoryId: 2,
      nameKr: '논커피',
      nameEn: 'non-coffee',
    },
    {
      categoryId: 3,
      nameKr: '디저트',
      nameEn: 'dessert',
    },
    {
      categoryId: 4,
      nameKr: '브런치',
      nameEn: 'brunch',
    },
    {
      categoryId: 5,
      nameKr: '스무디',
      nameEn: 'smoothie',
    },
    {
      categoryId: 6,
      nameKr: '티',
      nameEn: 'tea',
    },
  ],
  pageNumber: 1,
  totalPages: 1,
  totalElements: 6,
  pageSize: 10,
  first: true,
  last: true,
};

export { CATEGORY_COLUMNS, CATEGORY_LIST };
