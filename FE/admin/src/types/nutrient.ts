export type NutrientType = {
  nutrientTemplateId: number;
  nutrientTemplateName: string;
  nutrientTemplateNameEn: string;
  nutrientTemplateType: string;
};

export type NutrientDetailGetType = {
  nutritionId: number;
  nutritionValue: number;
  nutritionTemplateId: number;
  nutritionTemplateName: string;
  nutritionTemplateType: string;
};

export type NutritionDetailAddType = {
  nutritionTemplateId: number;
  nutritionValue: number;
};
