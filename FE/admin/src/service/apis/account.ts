import authClient from '@/service/authClient';
import { AccountForm, AccountType } from '@/types/account';
import { CustomError, PaginationResponse, Response } from '@/types/apiResponse';

export const getAccountList = async (
  keyword?: string,
  pageable: number = 1
): Promise<Response<PaginationResponse<AccountType>>> => {
  try {
    const params = keyword ? { keyword, pageable } : { pageable };
    const response = await authClient.get('/account', {
      params,
    });
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

export const postAccount = async (account: AccountForm) => {
  try {
    const response = await authClient.post('/account', account);
    return response.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
  }
};

export const deleteAccount = async (accountId: number) => {
  try {
    const response = await authClient.delete(`/account/${accountId}`);
    return response.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
  }
};

export const getAccountDetail = async () => {
  try {
    const response = await authClient.get(`/account/detail`);
    return response.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
  }
};

export const patchResetPassword = async (email: string, username: string) => {
  try {
    const response = await authClient.patch(`/account/pw`, {
      email,
      username,
    });
    return response.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
  }
};

export const patchAccount = async (account: AccountForm) => {
  try {
    const response = await authClient.patch('/account', account);
    return response.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
  }
};

export const patchAccountPassword = async (nowPw: string, newPw: string) => {
  try {
    const response = await authClient.patch(`/account/change_pw`, {
      nowPw,
      newPw,
    });
    return response.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
  }
};
