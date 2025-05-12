import { CustomError } from '@/types/apiResponse';
import authClient from '@/service/authClient';

async function getCategory(page?: number) {
  try {
    const res = await authClient.get(`/category?page=${page}`);
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

async function addCategory(nameKr: string, nameEn: string) {
  try {
    const res = await authClient.post('/category', {
      nameKr: nameKr,
      nameEn: nameEn,
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

async function editCategory(
  categoryId: number,
  nameKr: string,
  nameEn: string
) {
  try {
    const res = await authClient.patch(`/category/${categoryId}`, {
      nameKr: nameKr,
      nameEn: nameEn,
      status: 'REGISTERED',
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

export { getCategory, addCategory, editCategory };
