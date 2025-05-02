interface Menu {
  menu_id: number;
  image_url: string;
  name_kr: string;
  name_en: string;
  category: string;
  store_name: string;
  description: string;
  price: number;
  status: string;
  tags: string[];
}

interface MenuList {
  content: Menu[];
  page_number: number;
  total_pages: number;
  total_elements: number;
  page_size: number;
  first: boolean;
  last: boolean;
  error: string | null;
}

export type { Menu, MenuList };
