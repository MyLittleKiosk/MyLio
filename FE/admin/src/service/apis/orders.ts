import authClient from '@/service/authClient';
import { CustomError, PaginationResponse, Response } from '@/types/apiResponse';
import { OrderDetailType, OrderType } from '@/types/orders';

export async function getOrders(
  startDate?: string,
  endDate?: string,
  page?: number
): Promise<Response<PaginationResponse<OrderType>>> {
  try {
    const params = {
      startDate,
      endDate,
      page: page || 1,
    };

    const res = await authClient.get('/order_list', {
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

export async function getOrderDetail(
  orderId: string
): Promise<Response<OrderDetailType>> {
  try {
    const res = await authClient.get(`/order_list/${orderId}`);
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
