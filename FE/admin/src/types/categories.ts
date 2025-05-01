interface Category {
  category_id: number;
  name_kr: string;
  name_en: string;
}

interface CategoryList {
  success: boolean;
  data: {
    content: Category[];
    page_number: number;
    total_pages: number;
    total_elements: number;
    page_size: number;
    first: boolean;
    last: boolean;
  };
  timestamp: string;
}

export type { Category, CategoryList };
