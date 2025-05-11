import { CustomError } from '@/types/apiResponse';
import authClient from '@/service/authClient';

async function getMenus(page?: number, categoryId?: number) {
  try {
    const res = await authClient.get(
      `/menus?page=${page}&categoryId=${categoryId}`
    );
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

export default getMenus;
