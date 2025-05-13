import { CustomError } from '@/types/apiResponse';
import authClient from '@/service/authClient';

//키오스크 전체 조회 및 검색
const getKioskList = async (keyword?: string, page?: number) => {
  try {
    const res = await authClient.get('/kiosk', {
      params: { keyword, page },
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
};

//키오스크 등록
const addKiosk = async (name: string, startOrder: string) => {
  try {
    const res = await authClient.post('/kiosk', { name, startOrder });
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
};

//키오스크 상세조회
const getKioskDetail = async (kioskId: number) => {
  try {
    const res = await authClient.get(`/kiosk/${kioskId}`);
    return res.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
  }
};

//키오스크 삭제
const deleteKiosk = async (kioskId: number) => {
  try {
    const res = await authClient.delete(`/kiosk/${kioskId}`);
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
};

//키오스크 수정
const updateKiosk = async (
  kioskId: number,
  name: string,
  start_order: string
) => {
  try {
    const res = await authClient.patch(`/kiosk/${kioskId}`, {
      name,
      start_order,
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
};

export { getKioskList, addKiosk, getKioskDetail, deleteKiosk, updateKiosk };
