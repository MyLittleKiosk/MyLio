interface OptionInfo {
  option_id: number;
  is_required: boolean;
  option_detail_id: number;
}

interface OptionDetail {
  option_id: number;
  option_name_kr: string;
  option_name_en: string;
  option_detail: {
    option_detail_id: number;
    option_detail_value: string;
    additional_price: number;
  }[];
}

export type { OptionInfo, OptionDetail };
