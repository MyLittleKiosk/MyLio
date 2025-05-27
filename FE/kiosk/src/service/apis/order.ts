import { OrderRequest, OrderResponse } from '@/types/order';
import authClient from '@/service/authClient';
import { ApiResponse, CustomError } from '@/types/apiResponse';
import { PayRequest, PaySuccess, PaySuccessRequest } from '@/types/kakaoPay';
import { Pay } from '@/types/kakaoPay';

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

export async function requestPay(
  payRequest: PayRequest
): Promise<ApiResponse<Pay>> {
  try {
    const response = await authClient.post(
      '/pay/ready?pay_method=PAY',
      payRequest
    );
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

export async function postSuccess(
  paySuccessRequest: PaySuccessRequest,
  payMethod: string
): Promise<ApiResponse<PaySuccess>> {
  try {
    const response = await authClient.post(
      `/pay/success?pay_method=${payMethod}`,
      paySuccessRequest
    );
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
