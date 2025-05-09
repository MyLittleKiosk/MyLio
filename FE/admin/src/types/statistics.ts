export type SalesTrendType = {
  type: number;
  sales: number;
};

export type DailySalesStatisticsType = {
  totalSales: number;
  totalOrders: number;
};

export type PaymentSalesRatioType = {
  paymentName: string;
  ratio: number;
};

export type OrderSalesRatioType = {
  orderTypeName: string;
  ratio: number;
};

export type CategorySalesRatioType = {
  categoryName: string;
  ratio: number;
};
