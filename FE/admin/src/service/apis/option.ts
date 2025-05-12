import { CustomError } from '@/types/apiResponse';
import authClient from '@/service/authClient';

export async function getOptions() {
  try {
    const res = await authClient.get(`/option`);
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

//옵션 그룹 추가
export async function addOptionGroup({
  optionNameKr,
  optionNameEn,
}: {
  optionNameKr: string;
  optionNameEn: string;
}) {
  try {
    const res = await authClient.post('/option', {
      optionNameKr,
      optionNameEn,
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

export async function addOptionDetail({
  optionId,
  value,
  additionalPrice,
}: {
  optionId: number;
  value: string;
  additionalPrice: number;
}) {
  try {
    const res = await authClient.post(`/option_detail/${optionId}`, {
      value,
      additionalPrice,
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
