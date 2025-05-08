import { OptionList, OptionGroup } from '@/types/options';
import { Column } from '@/types/tableProps';

const OPTION_COLUMNS: Column<OptionGroup>[] = [
  {
    header: '옵션 그룹명',
    accessor: 'optionNameKr' as keyof OptionGroup,
  },
  {
    header: '옵션 항목',
    accessor: 'optionDetail' as keyof OptionGroup,
  },
  {
    header: '편집',
    accessor: 'edit' as keyof OptionGroup,
  },
  {
    header: '삭제',
    accessor: 'delete' as keyof OptionGroup,
  },
];

const OPTION_LIST: OptionList = {
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

export { OPTION_COLUMNS, OPTION_LIST };
