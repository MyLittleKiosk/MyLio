interface CategoryType {
  category_id: number;
  name_kr: string;
  name_en: string;
}

interface CategoryList {
  content: CategoryType[];
  page_number: number;
  total_pages: number;
  total_elements: number;
  page_size: number;
  first: boolean;
  last: boolean;
}

export type { CategoryType, CategoryList };
