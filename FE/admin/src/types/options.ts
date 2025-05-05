interface OptionInfoType {
  option_id: number;
  is_required: boolean;
  option_detail_id: number;
}

interface OptionType {
  option_id: number;
  option_name_kr: string;
  option_name_en: string;
  option_detail: {
    option_detail_id: number;
    option_detail_value: string;
    additional_price: number;
  }[];
}

interface OptionDetailType {
  option_detail_id: number;
  option_detail_value: string;
  additional_price: number;
}

interface OptionList {
  content: {
    options: OptionType[];
  };
}

export type { OptionInfoType, OptionDetailType, OptionType, OptionList };
