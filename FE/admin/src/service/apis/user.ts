import client from '@/service/client';
import { CustomError, Response } from '@/types/apiResponse';
import { User } from '@/types/user';

export async function login(
  email: string,
  password: string
): Promise<Response<User>> {
  try {
    const res = await client.post('/auth/login', { email, password });
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

export async function getRole(): Promise<Response<User>> {
  try {
    const res = await client.get('/accounts/role');
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
