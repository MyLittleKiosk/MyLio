import { IngredientType } from '@/types/ingredient';
import { Column } from '@/types/tableProps';

const INGREDIENT_COLUMNS: Column<IngredientType>[] = [
  {
    header: '이름',
    accessor: 'ingredientTemplateName' as keyof IngredientType,
  },
  {
    header: '영문 이름',
    accessor: 'ingredientTemplateNameEn' as keyof IngredientType,
  },
  {
    header: '편집',
    accessor: 'edit' as keyof IngredientType,
  },
];

const INGREDIENT_LIST = {
  content: [
    {
      ingredientTemplateId: 1,
      ingredientTemplateName: '에스프레스',
      ingredientTemplateNameEn: 'Espresso',
    },
    {
      ingredientTemplateId: 2,
      ingredientTemplateName: '우유',
      ingredientTemplateNameEn: 'Milk',
    },
    {
      ingredientTemplateId: 3,
      ingredientTemplateName: '바닐라시럽',
      ingredientTemplateNameEn: 'Vanilla Syrup',
    },
    {
      ingredientTemplateId: 4,
      ingredientTemplateName: '초콜릿 소스',
      ingredientTemplateNameEn: 'Chocolate Syrup',
    },
    {
      ingredientTemplateId: 5,
      ingredientTemplateName: '카라멜 시럽',
      ingredientTemplateNameEn: 'Caramel Syrup',
    },
  ],
};

export { INGREDIENT_COLUMNS, INGREDIENT_LIST };
