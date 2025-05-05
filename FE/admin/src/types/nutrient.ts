interface NutrientType {
  nutrient_template_id: number;
  name_kr: string;
  name_en: string;
}

interface NutrientList {
  content: NutrientType[];
  page_number: number;
  total_pages: number;
  total_elements: number;
  page_size: number;
}

export type { NutrientType, NutrientList };
