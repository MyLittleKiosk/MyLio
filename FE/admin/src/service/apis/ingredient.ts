import authClient from '@/service/authClient';
import { CustomError, PaginationResponse, Response } from '@/types/apiResponse';
import { IngredientType } from '@/types/ingredient';

export const getIngredientList = async (
  keyword?: string,
  page: number = 1
): Promise<Response<PaginationResponse<IngredientType>>> => {
  try {
    const params = keyword ? { keyword, page } : { page };
    const response = await authClient.get('/ingredient', { params });
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

export const postIngredient = async (ingredient: IngredientType) => {
  try {
    const response = await authClient.post('/ingredient', ingredient);
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

export const patchIngredient = async (ingredient: IngredientType) => {
  try {
    const response = await authClient.patch(
      `/ingredient/${ingredient.ingredientTemplateId}`,
      ingredient
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
};
