interface IngredientType {
  ingredient_id: number;
  name_kr: string;
  name_en: string;
}

interface IngredientList {
  content: IngredientType[];
  page_number: number;
  total_pages: number;
  total_elements: number;
  page_size: number;
}

export type { IngredientType, IngredientList };
