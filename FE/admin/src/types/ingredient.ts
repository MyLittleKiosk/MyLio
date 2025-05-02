interface Ingredient {
  ingredient_id: number;
  name_kr: string;
  name_en: string;
}

interface IngredientList {
  content: Ingredient[];
  page_number: number;
  total_pages: number;
  total_elements: number;
  page_size: number;
}

export type { Ingredient, IngredientList };
