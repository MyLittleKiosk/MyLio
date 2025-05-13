import authClient from '@/service/authClient';
import { CustomError, PaginationResponse, Response } from '@/types/apiResponse';
import { OrderType } from '@/types/orders';

export async function getOrders(
  startDate?: string,
  endDate?: string,
  pageable?: number
): Promise<Response<PaginationResponse<OrderType>>> {
  try {
    const params = {
      startDate,
      endDate,
      pageable: pageable || 1,
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
