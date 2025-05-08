import authClient from '@/service/authClient';
import { CustomError, Response } from '@/types/apiResponse';
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
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
    throw new Error('unknown error');
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
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
    throw new Error('unknown error');
  }
}

export async function getStatisticsByOrder(
  year: number,
  month?: number
): Promise<Response<OrderSalesRatioType[]>> {
  try {
    const params = month ? { year, month } : { year };
    const res = await authClient.get('/sales/by_order_type', {
      params,
    });
    return res.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
    throw new Error('unknown error');
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
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
    throw new Error('unknown error');
  }
}

export async function getStatisticsByDaily(): Promise<
  Response<DailySalesStatisticsType[]>
> {
  try {
    const res = await authClient.get('/sales/daily');
    return res.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
    throw new Error('unknown error');
  }
}
