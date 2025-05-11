import { OptionList } from '@/types/options';

export const OPTION_LIST: OptionList = {
  success: true,
  data: {
    options: [
      {
        optionId: 1,
        optionNameKr: '사이즈',
        optionNameEn: 'Size',
        optionDetail: [
          {
            optionDetailId: 1,
            optionDetailValue: 'Small',
            additionalPrice: 0,
          },
          {
            optionDetailId: 2,
            optionDetailValue: 'Medium',
            additionalPrice: 500,
          },
          {
            optionDetailId: 3,
            optionDetailValue: 'Large',
            additionalPrice: 700,
          },
        ],
      },
    ],
  },
  timestamp: '2024-01-01T00:00:00.000Z',
};
