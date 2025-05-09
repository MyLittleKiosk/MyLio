import client from '@/service/client';
import { ApiResponse } from '@/types/apiResponse';
import type { User } from '@/types/user';

export const login = async (
  email: string,
  password: string,
  kioskId: string
): Promise<ApiResponse<User>> => {
  try {
    const response = await client.post('/auth/login', {
      email,
      password,
      kioskId,
    });
    return response.data;
  } catch (error: unknown) {
    console.error(error);
    throw error;
  }
};
