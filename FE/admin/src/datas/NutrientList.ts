import { NutrientType } from '@/types/nutrient';
import { Column } from '@/types/tableProps';

const NUTRIENT_COLUMNS: Column<NutrientType>[] = [
  {
    header: '영양소명',
    accessor: 'nutrientTemplateName' as keyof NutrientType,
  },
  {
    header: '단위',
    accessor: 'nutrientTemplateType' as keyof NutrientType,
  },
  {
    header: '편집',
    accessor: 'edit' as keyof NutrientType,
  },
];

const NUTRIENT_LIST = {
  content: [
    {
      nutrientTemplateId: 1,
      nutrientTemplateName: '칼로리',
      nutrientTemplateNameEn: 'Calories',
      nutrientTemplateType: 'kcal',
    },
    {
      nutrientTemplateId: 2,
      nutrientTemplateName: '단백질',
      nutrientTemplateNameEn: 'Protein',
      nutrientTemplateType: 'g',
    },
    {
      nutrientTemplateId: 3,
      nutrientTemplateName: '지방',
      nutrientTemplateNameEn: 'Fat',
      nutrientTemplateType: 'g',
    },
    {
      nutrientTemplateId: 4,
      nutrientTemplateName: '탄수화물',
      nutrientTemplateNameEn: 'Carbohydrate',
      nutrientTemplateType: 'g',
    },
  ],
};

export { NUTRIENT_COLUMNS, NUTRIENT_LIST };
