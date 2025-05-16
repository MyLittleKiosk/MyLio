import { CustomError, PaginationResponse, Response } from '@/types/apiResponse';
import { NutrientType, NutritionTemplateAddType } from '@/types/nutrient';
import authClient from '@/service/authClient';

export async function getNutritionList(
  keyword?: string,
  page: number = 1
): Promise<Response<PaginationResponse<NutrientType>>> {
  try {
    const params = keyword ? { keyword, page } : { page };
    const response = await authClient.get('/nutrition', { params });
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

export async function addNutritionTemplate(
  nutrition: NutritionTemplateAddType
) {
  try {
    const response = await authClient.post('/nutrition', nutrition);
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
