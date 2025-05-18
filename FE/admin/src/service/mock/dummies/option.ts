import { OptionGroup } from '@/types/options';
import { PaginationResponse, Response } from '@/types/apiResponse';

export const OPTION_LIST: Response<PaginationResponse<OptionGroup>> = {
  success: true,
  data: {
    content: [
      {
        optionId: 1,
        optionNameKr: '사이즈',
        optionNameEn: 'Size',
        optionDetails: [
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
    pageNumber: 1,
    totalPages: 1,
    totalElements: 1,
    pageSize: 1,
    first: true,
    last: true,
  },
  timestamp: '2024-01-01T00:00:00.000Z',
};
