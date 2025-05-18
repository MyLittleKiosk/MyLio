import { CustomError } from '@/types/apiResponse';
import authClient from '@/service/authClient';

//옵션 전체 조회
export async function getOptions(
  keyword?: string,
  page?: number,
  size?: number
) {
  const params = {
    keyword: keyword || null,
    page: page || 1,
    size: size || 50,
  };
  try {
    const res = await authClient.get(`/option`, { params });
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
export async function editOptionGroup(
  optionId: number,
  optionNameKr: string,
  optionNameEn: string
) {
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
export async function deleteOptionGroup(optionId: number) {
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

//옵션 상세 조회
export async function getOptionDetail(optionId: number) {
  try {
    const res = await authClient.get(`/option_detail/${optionId}`);
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
export async function addOptionDetail(
  optionId: number,
  value: string,
  additionalPrice: number
) {
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
export async function editOptionDetail(
  optionDetailId: number,
  value: string,
  additionalPrice: number
) {
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
export async function deleteOptionDetail(optionDetailId: number) {
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
