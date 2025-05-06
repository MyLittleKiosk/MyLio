import OrderItem from '@/types/orders';
import { Column } from '@/types/tableProps';

const ORDER_COLUMNS: Column<OrderItem>[] = [
  { header: '주문번호', accessor: 'order_id' as keyof OrderItem },
  { header: '점포', accessor: 'order_store' as keyof OrderItem },
  { header: '날짜/시간', accessor: 'order_date' as keyof OrderItem },
  { header: '금액', accessor: 'order_price' as keyof OrderItem },
  { header: '유형', accessor: 'order_type' as keyof OrderItem },
  { header: '결제방법', accessor: 'order_payment' as keyof OrderItem },
];

const ORDER_LIST = {
  content: [
    {
      order_id: 'ORD-001234',
      order_store: 'MyLio 강남점',
      order_date: '2023-04-22 14:30:00',
      order_price: 15500,
      order_type: '매장',
      order_payment: '신용카드',
    },
    {
      order_id: 'ORD-001235',
      order_store: 'MyLio 홍대점',
      order_date: '2023-04-22 15:45:00',
      order_price: 12000,
      order_type: '포장',
      order_payment: '간편결제',
    },
    {
      order_id: 'ORD-001236',
      order_store: 'MyLio 명동점',
      order_date: '2023-04-22 16:30:00',
      order_price: 9000,
      order_type: '포장',
      order_payment: '현금',
    },
    {
      order_id: 'ORD-001237',
      order_store: 'MyLio 여의도점',
      order_date: '2023-04-22 17:15:00',
      order_price: 18500,
      order_type: '매장',
      order_payment: '신용카드',
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

export { ORDER_COLUMNS, ORDER_LIST };
