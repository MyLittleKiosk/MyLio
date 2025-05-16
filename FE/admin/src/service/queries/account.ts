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
import {
  QueryClient,
  useMutation,
  useSuspenseQuery,
} from '@tanstack/react-query';

export const useGetAccountList = () => {
  const query = useSuspenseQuery({
    queryKey: ['accountList'],
    queryFn: () => getAccountList(),
  });

  return {
    data: query.data?.data.content,
  };
};

export const usePostAccount = () => {
  const queryClient = new QueryClient();
  const query = useMutation({
    mutationFn: ({ account }: { account: AccountForm }) => postAccount(account),
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

export const useDeleteAccount = () => {
  const queryClient = new QueryClient();
  const query = useMutation({
    mutationFn: ({ accountId }: { accountId: number }) =>
      deleteAccount(accountId),
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

export const useGetAccountDetail = () => {
  const query = useSuspenseQuery({
    queryKey: ['accountDetail'],
    queryFn: () => getAccountDetail(),
  });

  return {
    data: query.data?.data,
  };
};

export const usePatchAccount = () => {
  const queryClient = new QueryClient();
  const query = useMutation({
    mutationFn: ({ account }: { account: AccountForm }) =>
      patchAccount(account),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accountDetail'] });
    },
  });

  return {
    mutate: query.mutate,
    isPending: query.isPending,
    isError: query.isError,
    isSuccess: query.isSuccess,
  };
};

export const usePatchAccountPassword = () => {
  const query = useMutation({
    mutationFn: ({
      nowPassword,
      newPassword,
    }: {
      nowPassword: string;
      newPassword: string;
    }) => patchAccountPassword(nowPassword, newPassword),
  });

  return {
    mutate: query.mutate,
    isPending: query.isPending,
    isError: query.isError,
    isSuccess: query.isSuccess,
  };
};

export const usePatchResetPassword = (email: string, username: string) => {
  const query = useMutation({
    mutationFn: () => patchResetPassword(email, username),
  });

  return {
    mutate: query.mutate,
    isPending: query.isPending,
    isError: query.isError,
    isSuccess: query.isSuccess,
  };
};
