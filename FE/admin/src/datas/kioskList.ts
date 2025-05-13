import { PaginationResponse } from '@/types/apiResponse';
import { KioskType } from '@/types/kiosk';
import { Column } from '@/types/tableProps';

const KIOSK_COLUMNS: Column<KioskType>[] = [
  { header: '키오스크명', accessor: 'name' as keyof KioskType },
  { header: '키오스크 ID', accessor: 'kioskId' as keyof KioskType },
  { header: '상태', accessor: 'isActivate' as keyof KioskType },
  { header: '편집', accessor: 'edit' as keyof KioskType },
  { header: '삭제', accessor: 'delete' as keyof KioskType },
];

const KIOSK_LIST: PaginationResponse<KioskType> = {
  content: [
    {
      name: '키오스크 A',
      kioskId: 1,
      startOrder: 'A',
      isActivate: true,
    },
    {
      name: '키오스크 B',
      kioskId: 2,
      startOrder: 'B',
      isActivate: true,
    },
    {
      name: '키오스크 C',
      kioskId: 3,
      startOrder: 'C',
      isActivate: false,
    },
    {
      name: '키오스크 D',
      kioskId: 4,
      startOrder: 'D',
      isActivate: true,
    },
  ],
  pageNumber: 1,
  totalPages: 1,
  totalElements: 4,
  pageSize: 10,
  first: true,
  last: true,
};

export { KIOSK_COLUMNS, KIOSK_LIST };
