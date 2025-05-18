import { CustomError } from '@/types/apiResponse';
import authClient from '@/service/authClient';

async function getCategory(keyword?: string, page?: number) {
  const params = {
    keyword: keyword || null,
    page: page || 1,
  };
  try {
    const res = await authClient.get(`/category`, {
      params,
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

async function deleteCategory(categoryId: number) {
  try {
    const res = await authClient.delete(`/category/${categoryId}`);
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

export { getCategory, addCategory, editCategory, deleteCategory };
