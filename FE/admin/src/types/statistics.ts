type SalesTrendType = {
  type: number;
  sales: number;
};

type DailySalesStatisticsType = {
  totalSales: number;
  totalOrders: number;
};

type PaymentSalesRatioType = {
  paymentName: string;
  ratio: number;
};

type OrderSalesRatioType = {
  orderTypeName: string;
  ratio: number;
};

type CategorySalesRatioType = {
  categoryName: string;
  ratio: number;
};

export type {
  CategorySalesRatioType,
  DailySalesStatisticsType,
  OrderSalesRatioType,
  PaymentSalesRatioType,
  SalesTrendType,
};
