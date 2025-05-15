export type IngredientForm = {
  ingredientTemplateName: string;
  ingredientTemplateNameEn: string;
};

export type IngredientType = IngredientForm & {
  ingredientTemplateId: number;
};
