import { CustomError } from '@/types/apiResponse';
import authClient from '@/service/authClient';

export async function getCategory(pageable: number) {
  try {
    const response = await authClient.get(`/category?pageable=${pageable}`);
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
