import { client } from '@/service/client';
import { CustomError } from '@/types/apiResponse';

export async function login(email: string, password: string) {
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
