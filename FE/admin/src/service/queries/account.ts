import { AccountForm } from '@/types/account';
import {
  deleteAccount,
  getAccountDetail,
  getAccountList,
  patchAccount,
  patchAccountPassword,
  patchResetPassword,
  postAccount,
} from '@services/apis/account';
import { QueryClient, useMutation, useQuery } from '@tanstack/react-query';

export const useGetAccountList = () => {
  const query = useQuery({
    queryKey: ['accountList'],
    queryFn: () => getAccountList(),
  });

  return {
    data: query.data?.data.content,
    isLoading: query.isLoading,
    isError: query.isError,
  };
};

export const usePostAccount = (account: AccountForm) => {
  const queryClient = new QueryClient();
  const query = useMutation({
    mutationFn: () => postAccount(account),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accountList'] });
    },
  });

  return {
    mutate: query.mutate,
    isPending: query.isPending,
    isError: query.isError,
  };
};

export const useDeleteAccount = (accountId: number) => {
  const queryClient = new QueryClient();
  const query = useMutation({
    mutationFn: () => deleteAccount(accountId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accountList'] });
    },
  });

  return {
    mutate: query.mutate,
    isPending: query.isPending,
    isError: query.isError,
  };
};

export const useGetAccountDetail = (accountId: number) => {
  const query = useQuery({
    queryKey: ['accountDetail', accountId],
    queryFn: () => getAccountDetail(accountId),
  });

  return {
    data: query.data?.data,
    isLoading: query.isLoading,
    isError: query.isError,
  };
};

export const usePatchAccount = (accountId: number, account: AccountForm) => {
  const queryClient = new QueryClient();
  const query = useMutation({
    mutationFn: () => patchAccount(accountId, account),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accountList'] });
    },
  });

  return {
    mutate: query.mutate,
    isPending: query.isPending,
    isError: query.isError,
  };
};

export const usePatchAccountPassword = (nowPw: string, newPw: string) => {
  const queryClient = new QueryClient();
  const query = useMutation({
    mutationFn: () => patchAccountPassword(nowPw, newPw),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accountList'] });
    },
  });

  return {
    mutate: query.mutate,
    isPending: query.isPending,
    isError: query.isError,
  };
};

export const usePatchResetPassword = (email: string, username: string) => {
  const queryClient = new QueryClient();
  const query = useMutation({
    mutationFn: () => patchResetPassword(email, username),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accountList'] });
    },
  });

  return {
    mutate: query.mutate,
    isPending: query.isPending,
    isError: query.isError,
  };
};
