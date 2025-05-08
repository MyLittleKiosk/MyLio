import { CategoryType } from '@/types/categories';
import { OptionInfoType, OptionType } from '@/types/options';
import { Column } from '@/types/tableProps';

interface MenuType {
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
  content: MenuType[];
  page_number: number;
  total_pages: number;
  total_elements: number;
  page_size: number;
  first: boolean;
  last: boolean;
}

interface TagType {
  tag_kr: string;
  tag_en: string;
}

interface NutritionInfoType {
  nutrition_template_id: number;
  nutrition_value: number;
}

interface MenuAdd {
  image_url: string;
  name_kr: string;
  name_en: string;
  category_id: number;
  description: string;
  price: number;
  tags: TagType[];
  nutrition_info: NutritionInfoType[];
  ingredient_info: number[];
  option_info: OptionInfoType[];
}

type NavItemType =
  | {
      title: string;
      columns: Column<MenuType>[];
    }
  | {
      title: string;
      columns: Column<CategoryType>[];
    }
  | {
      title: string;
      columns: Column<OptionType>[];
    };

export type { MenuType, MenuList, MenuAdd, NavItemType };
