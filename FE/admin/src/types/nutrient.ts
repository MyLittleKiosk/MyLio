export type NutrientType = {
  nutritionTemplateId: number;
  nutritionTemplateName: string;
  nutritionTemplateNameEn: string;
  nutritionTemplateType: string;
};

export type NutritionTemplateAddType = {
  nutritionTemplateName: string;
  nutritionTemplateNameEn: string;
  nutritionTemplateType: string;
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
