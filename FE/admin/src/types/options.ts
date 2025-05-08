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

export type OptionType = {
  optionId: number;
  optionNameKr: string;
  optionNameEn: string;
  optionDetail: OptionDetailType[];
};
