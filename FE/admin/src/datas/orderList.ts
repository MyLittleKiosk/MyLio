import { PaginationResponse } from '@/types/apiResponse';
import { OrderType } from '@/types/orders';
import { Column } from '@/types/tableProps';

const ORDER_COLUMNS: Column<OrderType>[] = [
  { header: '주문번호', accessor: 'orderId' as keyof OrderType },
  { header: '날짜/시간', accessor: 'orderedAt' as keyof OrderType },
  { header: '금액', accessor: 'totalPrice' as keyof OrderType },
  { header: '유형', accessor: 'orderType' as keyof OrderType },
  { header: '결제방법', accessor: 'paidBy' as keyof OrderType },
];

const ORDER_LIST: PaginationResponse<OrderType> = {
  content: [
    {
      orderId: 'ORD-001234',
      orderedAt: '2023-04-22 14:30:00',
      totalPrice: 15500,
      orderType: '매장',
      paidBy: '신용카드',
    },
    {
      orderId: 'ORD-001235',
      orderedAt: '2023-04-22 15:45:00',
      totalPrice: 12000,
      orderType: '포장',
      paidBy: '간편결제',
    },
    {
      orderId: 'ORD-001236',
      orderedAt: '2023-04-22 16:30:00',
      totalPrice: 9000,
      orderType: '포장',
      paidBy: '현금',
    },
    {
      orderId: 'ORD-001237',
      orderedAt: '2023-04-22 17:15:00',
      totalPrice: 18500,
      orderType: '매장',
      paidBy: '신용카드',
    },
  ],
  pageNumber: 1,
  totalPages: 1,
  totalElements: 4,
  pageSize: 10,
  first: true,
  last: true,
};

const DETAIL_ORDERS = {
  content: [
    {
      productName: '아메리카노',
      productPrice: 4500,
      productQuantity: 1,
      productOption: 'ICE, 샷추가',
    },
    {
      productName: '카페라떼',
      productPrice: 4500,
      productQuantity: 1,
      productOption: '',
    },
  ],
};

export { DETAIL_ORDERS, ORDER_COLUMNS, ORDER_LIST };
