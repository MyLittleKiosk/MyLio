import { Column } from '@/types/tableProps';

interface KioskItem {
  name: string;
  id: string;
  status: boolean;
}

const KIOSK_COLUMNS: Column<KioskItem>[] = [
  { header: '키오스크명', accessor: 'name' as keyof KioskItem },
  { header: '키오스크 ID', accessor: 'id' as keyof KioskItem },
  { header: '상태', accessor: 'status' as keyof KioskItem },
  { header: '편집', accessor: 'edit' as keyof KioskItem },
  { header: '삭제', accessor: 'delete' as keyof KioskItem },
];

const KIOSK_LIST = {
  content: [
    {
      name: '키오스크 A',
      id: 'kiosk_001',
      status: true,
    },
    {
      name: '키오스크 B',
      id: 'kiosk_002',
      status: true,
    },
    {
      name: '키오스크 C',
      id: 'kiosk_003',
      status: false,
    },
    {
      name: '키오스크 D',
      id: 'kiosk_004',
      status: true,
    },
  ],
  page_number: 1,
  total_pages: 1,
  total_elements: 4,
  page_size: 10,
  first: true,
  last: true,
  error: null,
};

export { KIOSK_COLUMNS, KIOSK_LIST };
