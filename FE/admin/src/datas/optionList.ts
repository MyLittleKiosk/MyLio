import { OptionList, OptionType } from '@/types/options';
import { Column } from '@/types/tableProps';

const OPTION_COLUMNS: Column<OptionType>[] = [
  {
    header: '옵션 그룹명',
    accessor: 'option_name_kr' as keyof OptionType,
  },
  {
    header: '옵션 항목',
    accessor: 'option_detail' as keyof OptionType,
  },
  {
    header: '편집',
    accessor: 'edit' as keyof OptionType,
  },
  {
    header: '삭제',
    accessor: 'delete' as keyof OptionType,
  },
];

const OPTION_LIST: OptionList = {
  content: {
    options: [
      {
        option_id: 1,
        option_name_kr: '사이즈',
        option_name_en: 'Size',
        option_detail: [
          {
            option_detail_id: 1,
            option_detail_value: 'Small',
            additional_price: 0,
          },
          {
            option_detail_id: 2,
            option_detail_value: 'Medium',
            additional_price: 500,
          },
          {
            option_detail_id: 3,
            option_detail_value: 'Large',
            additional_price: 700,
          },
        ],
      },
    ],
  },
};

export { OPTION_COLUMNS, OPTION_LIST };
