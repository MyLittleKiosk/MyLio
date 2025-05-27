import { NutrientType } from '@/types/nutrient';
import { Column } from '@/types/tableProps';

const NUTRIENT_COLUMNS: Column<NutrientType>[] = [
  {
    header: '영양소명',
    accessor: 'nutritionTemplateName' as keyof NutrientType,
  },
  {
    header: '단위',
    accessor: 'nutritionTemplateType' as keyof NutrientType,
  },
  {
    header: '편집',
    accessor: 'edit' as keyof NutrientType,
  },
];

const NUTRIENT_LIST = {
  content: [
    {
      nutritionTemplateId: 1,
      nutritionTemplateName: '칼로리',
      nutritionTemplateNameEn: 'Calories',
      nutritionTemplateType: 'kcal',
    },
    {
      nutritionTemplateId: 2,
      nutritionTemplateName: '단백질',
      nutritionTemplateNameEn: 'Protein',
      nutritionTemplateType: 'g',
    },
    {
      nutritionTemplateId: 3,
      nutritionTemplateName: '지방',
      nutritionTemplateNameEn: 'Fat',
      nutritionTemplateType: 'g',
    },
    {
      nutritionTemplateId: 4,
      nutritionTemplateName: '탄수화물',
      nutritionTemplateNameEn: 'Carbohydrate',
      nutritionTemplateType: 'g',
    },
  ],
  pageNumber: 1,
  totalPages: 1,
  totalElements: 4,
  pageSize: 10,
  first: true,
  last: false,
};

export { NUTRIENT_COLUMNS, NUTRIENT_LIST };
