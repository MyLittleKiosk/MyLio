import { OrderRequest, OrderResponse } from '@/types/order';
import authClient from '@/service/authClient';
import { ApiResponse, CustomError } from '@/types/apiResponse';

export async function postOrder(
  order: OrderRequest
): Promise<ApiResponse<OrderResponse>> {
  try {
    const response = await authClient.post('/order', order);
    return response.data;
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
