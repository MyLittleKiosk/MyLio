import { PaginationResponse, Response } from '@/types/apiResponse';
import { CategoryType } from '@/types/categories';

const CATEGORY_LIST: Response<PaginationResponse<CategoryType>> = {
  success: true,
  data: {
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
  },
  timestamp: '2025-05-08T00:43:04.030570785',
};

export { CATEGORY_LIST };
