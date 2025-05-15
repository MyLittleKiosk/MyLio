import client from '@/service/client';
import { ApiResponse, CustomError } from '@/types/apiResponse';
import type { User } from '@/types/user';
import authClient from '../authClient';

export async function login(
  email: string,
  password: string,
  kioskId: number
): Promise<ApiResponse<User>> {
  try {
    const response = await client.post('/auth/login/kiosk', {
      email,
      password,
      kioskId,
    });
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

export async function logout(kioskId: number): Promise<ApiResponse<void>> {
  try {
    const response = await authClient.post('/auth/logout', {
      kioskId,
    });
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

export async function refresh(): Promise<ApiResponse<User>> {
  try {
    const response = await client.post('/auth/refresh');
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
