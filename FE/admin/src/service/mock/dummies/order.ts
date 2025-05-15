const DUMMY_ORDER_LIST = {
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
  ],
  pageNumber: 1,
  totalPages: 3,
  totalElements: 10,
  pageSize: 5,
  first: true,
  last: false,
};
export default DUMMY_ORDER_LIST;
