import authClient from '@/service/authClient';
import { Response } from '@/types/apiResponse';
import {
  CategorySalesRatioType,
  DailySalesStatisticsType,
  OrderSalesRatioType,
  PaymentSalesRatioType,
  SalesTrendType,
} from '@/types/statistics';

export async function getSalesTrend(
  year: number,
  month?: number
): Promise<Response<SalesTrendType[]>> {
  try {
    const params = month ? { year, month } : { year };
    const res = await authClient.get('/sales', {
      params,
    });
    return res.data;
  } catch (e: unknown) {
    if (e instanceof Error) throw new Error(e.message);
    else throw new Error('unknown Error');
  }
}

export async function getStatisticsByCategory(
  year: number,
  month?: number
): Promise<Response<CategorySalesRatioType[]>> {
  try {
    const params = month ? { year, month } : { year };
    const res = await authClient.get('/sales/by_category', {
      params,
    });
    return res.data;
  } catch (e: unknown) {
    if (e instanceof Error) throw new Error(e.message);
    else throw new Error('unknown Error');
  }
}

export async function getStatisticsByOrder(
  year: number,
  month?: number
): Promise<Response<OrderSalesRatioType[]>> {
  try {
    const params = month ? { year, month } : { year };
    const res = await authClient.get('/sales/by_order', {
      params,
    });
    return res.data;
  } catch (e: unknown) {
    if (e instanceof Error) throw new Error(e.message);
    else throw new Error('unknown Error');
  }
}

export async function getStatisticsByPayment(
  year: number,
  month?: number
): Promise<Response<PaymentSalesRatioType[]>> {
  try {
    const params = month ? { year, month } : { year };
    const res = await authClient.get('/sales/by_payment', {
      params,
    });
    return res.data;
  } catch (e: unknown) {
    if (e instanceof Error) throw new Error(e.message);
    else throw new Error('unknown Error');
  }
}

export async function getStatisticsByDaily(): Promise<
  Response<DailySalesStatisticsType[]>
> {
  try {
    const res = await authClient.get('/sales/by_daily');
    return res.data;
  } catch (e: unknown) {
    if (e instanceof Error) throw new Error(e.message);
    else throw new Error('unknown Error');
  }
}
