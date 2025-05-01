import { CategoryList } from '@/types/categories';

const CATEGORY_LIST: CategoryList = {
  success: true,
  data: {
    content: [
      {
        category_id: 1,
        name_kr: '커피',
        name_en: 'coffee',
      },
      {
        category_id: 2,
        name_kr: '논커피',
        name_en: 'non-coffee',
      },
      {
        category_id: 3,
        name_kr: '디저트',
        name_en: 'dessert',
      },
      {
        category_id: 4,
        name_kr: '브런치',
        name_en: 'brunch',
      },
      {
        category_id: 5,
        name_kr: '스무디',
        name_en: 'smoothie',
      },
      {
        category_id: 6,
        name_kr: '티',
        name_en: 'tea',
      },
    ],
    page_number: 1,
    total_pages: 1,
    total_elements: 6,
    page_size: 10,
    first: true,
    last: true,
  },
  timestamp: '2025-05-01T09:45:14.631956',
};

export default CATEGORY_LIST;
