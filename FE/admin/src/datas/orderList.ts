import { PaginationResponse } from '@/types/apiResponse';
import { OrderType } from '@/types/orders';
import { Column } from '@/types/tableProps';

const ORDER_COLUMNS: Column<OrderType>[] = [
  { header: '주문번호', accessor: 'orderId' as keyof OrderType },
  { header: '점포', accessor: 'orderStore' as keyof OrderType },
  { header: '날짜/시간', accessor: 'orderDate' as keyof OrderType },
  { header: '금액', accessor: 'orderPrice' as keyof OrderType },
  { header: '유형', accessor: 'orderType' as keyof OrderType },
  { header: '결제방법', accessor: 'orderPayment' as keyof OrderType },
];

const ORDER_LIST: PaginationResponse<OrderType> = {
  content: [
    {
      orderId: 'ORD-001234',
      orderStore: 'MyLio 강남점',
      orderDate: '2023-04-22 14:30:00',
      orderPrice: 15500,
      orderType: '매장',
      orderPayment: '신용카드',
    },
    {
      orderId: 'ORD-001235',
      orderStore: 'MyLio 홍대점',
      orderDate: '2023-04-22 15:45:00',
      orderPrice: 12000,
      orderType: '포장',
      orderPayment: '간편결제',
    },
    {
      orderId: 'ORD-001236',
      orderStore: 'MyLio 명동점',
      orderDate: '2023-04-22 16:30:00',
      orderPrice: 9000,
      orderType: '포장',
      orderPayment: '현금',
    },
    {
      orderId: 'ORD-001237',
      orderStore: 'MyLio 여의도점',
      orderDate: '2023-04-22 17:15:00',
      orderPrice: 18500,
      orderType: '매장',
      orderPayment: '신용카드',
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

export { ORDER_COLUMNS, ORDER_LIST, DETAIL_ORDERS };
