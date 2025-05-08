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

export interface OptionList {
  success: boolean;
  data: {
    options: OptionGroup[];
  };
  timestamp: string;
}
