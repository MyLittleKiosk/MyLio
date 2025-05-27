import { CategoryType } from '@/types/categories';
import {
  OptionInfoType,
  OptionGroup,
  OptionDetailGetType,
} from '@/types/options';
import { Column } from '@/types/tableProps';
import { NutritionDetailAddType, NutritionMenuGetType } from '@/types/nutrient';
import { TagDetailGetType, TagType } from '@/types/tags';
import { IngredientDetailGetType } from './ingredient';

export type MenuType = {
  menuId: number;
  nameKr: string;
  nameEn: string;
  category: string;
  storeName: string;
  description: string;
  price: number;
  status: string;
  tags: string[];
};

export type MenuResponseType = {
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

export type MenuDetailGetType = {
  menuInfo: {
    menuId: number;
    imageUrl: string;
    nameKr: string;
    nameEn: string;
    category: string;
    storeName: string;
    description: string;
    price: number;
    status: string;
  };
  tags: TagDetailGetType[];
  nutritionInfo: NutritionMenuGetType[];
  ingredientInfo: IngredientDetailGetType[];
  optionInfo: OptionDetailGetType[];
};

export interface MenuAdd {
  nameKr: string;
  nameEn: string;
  categoryId: number;
  description: string;
  price: number;
  tags: TagType[];
  nutritionInfo: NutritionDetailAddType[];
  ingredientInfo: number[];
  optionInfo: OptionInfoType[];
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
      columns: Column<OptionGroup>[];
    };
