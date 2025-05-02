interface Category {
  category_id: number;
  name_kr: string;
  name_en: string;
}

interface CategoryList {
  content: Category[];
  page_number: number;
  total_pages: number;
  total_elements: number;
  page_size: number;
  first: boolean;
  last: boolean;
}

export type { Category, CategoryList };
