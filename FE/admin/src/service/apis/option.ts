import { CustomError } from '@/types/apiResponse';
import authClient from '@/service/authClient';

//옵션 전체 조회
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

//옵션 그룹명 수정
export async function editOptionGroup({
  optionId,
  optionNameKr,
  optionNameEn,
}: {
  optionId: number;
  optionNameKr: string;
  optionNameEn: string;
}) {
  try {
    const res = await authClient.patch(`/option/${optionId}`, {
      optionNameKr,
      optionNameEn,
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

//옵션 그룹 삭제
export async function deleteOptionGroup({ optionId }: { optionId: number }) {
  try {
    const res = await authClient.delete(`/option/${optionId}`);
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

//옵션 상세 추가
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

//옵션 상세 수정
export async function editOptionDetail({
  optionDetailId,
  value,
  additionalPrice,
}: {
  optionDetailId: number;
  value: string;
  additionalPrice: number;
}) {
  try {
    const res = await authClient.patch(`/option_detail/${optionDetailId}`, {
      value,
      additionalPrice,
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

//옵션 상세 삭제
export async function deleteOptionDetail({
  optionDetailId,
}: {
  optionDetailId: number;
}) {
  try {
    const res = await authClient.delete(`/option_detail/${optionDetailId}`);
    return res.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
  }
}
