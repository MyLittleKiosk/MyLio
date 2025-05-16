export type NutrientType = {
  nutrientTemplateId: number;
  nutrientTemplateName: string;
  nutrientTemplateNameEn: string;
  nutrientTemplateType: string;
};

export type NutritionTemplateAddType = {
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

export type NutritionMenuGetType = {
  nutritionId: number;
  nutritionName: string;
  nutritionValue: number;
  nutritionType: string;
};

export type NutritionDetailAddType = {
  nutritionTemplateId: number;
  nutritionValue: number;
};
