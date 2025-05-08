import { OptionGroup } from '@/types/options';
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

export { OPTION_COLUMNS };
