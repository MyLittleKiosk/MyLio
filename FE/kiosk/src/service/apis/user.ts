import client from '@/service/client';
import { ApiResponse, CustomError } from '@/types/apiResponse';
import type { User } from '@/types/user';

export const login = async (
  email: string,
  password: string,
  kioskId: number
): Promise<ApiResponse<User>> => {
  try {
    const response = await client.post('/auth/login', {
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
};
