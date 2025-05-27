export type OrderType = {
  orderId: string;
  orderedAt: string;
  totalPrice: number;
  orderType: string;
  paidBy: string;
};

export type OrderDetailType = OrderType & {
  orderItems: OrderItem[];
};

export type OrderItem = {
  itemName: string;
  quantity: number;
  price: number;
  options: string[];
};
