export type NutrientType = {
  nutrientTemplateId: number;
  nameKr: string;
  nameEn: string;
};

export type NutrientDetailGetType = {
  nutritionId: number;
  nutritionName: string;
  nutritionValue: number;
  nutritionType: string;
};

export type NutritionInfoType = {
  nutritionTemplateId: number;
  nutritionValue: number;
};
