import { CategoryType } from '@/types/categories';
import { OptionInfoType, OptionType } from '@/types/options';
import { Column } from '@/types/tableProps';
import { NutritionInfoType } from '@/types/nutrient';
import { TagType } from '@/types/tags';

export type MenuType = {
  menuId: number;
  imageUrl: string;
  nameKr: string;
  nameEn: string;
  category: string;
  storeName: string;
  description: string;
  price: number;
  status: string;
  tags: string[];
};

export interface MenuAdd {
  imageUrl: string;
  nameKr: string;
  nameEn: string;
  categoryId: number;
  description: string;
  price: number;
  tags: TagType[];
  nutrition_info: NutritionInfoType[];
  ingredient_info: number[];
  option_info: OptionInfoType[];
}

export type NavItemType =
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
