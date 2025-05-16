export type IngredientForm = {
  ingredientTemplateName: string;
  ingredientTemplateNameEn: string;
};

export type IngredientType = IngredientForm & {
  ingredientTemplateId: number;
};

export type IngredientDetailGetType = {
  menuIngredientId: number;
  ingredientId: number;
  ingredientNameKr: string;
  ingredientNameEn: string;
};
