export type OptionInfoType = {
  optionId: number;
  isRequired: boolean;
  optionDetailId: number;
};

export type OptionDetailType = {
  optionDetailId: number;
  optionDetailValue: string;
  additionalPrice: number;
};

export interface OptionGroup {
  optionId: number;
  optionNameKr: string;
  optionNameEn: string;
  optionDetail: OptionDetailType[];
}

export type OptionDetailGetType = {
  menuOptionId: number;
  optionId: number;
  optionNameKr: string;
  optionNameEn: string;
  optionValue: string;
  additionalPrice: number;
  required: boolean;
};

export interface OptionList {
  success: boolean;
  data: {
    options: OptionGroup[];
  };
  timestamp: string;
}
