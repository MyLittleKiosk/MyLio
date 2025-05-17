import { getRole, login, logout } from '@/service/apis/user';
import { useUserStore } from '@/stores/useUserStore';
import { Response } from '@/types/apiResponse';
import { User } from '@/types/user';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';

const useLogin = () => {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { setUser } = useUserStore();

  return useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      login(email, password),
    onSuccess: (data: Response<User>) => {
      setUser(data.data);
      queryClient.setQueryData(['role'], data);
      navigate(data.data?.role === 'SUPER' ? '/accounts' : '/');
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

const useGetRole = () => {
  const query = useQuery<Response<User>>({
    queryKey: ['role'],
    queryFn: getRole,
    retry: false,
  });

  return {
    data: query.data,
    isLoading: query.isLoading,
    isError: query.isError,
    error: query.error,
  };
};

const useLogout = () => {
  const navigate = useNavigate();
  const { logout: setUserLogout } = useUserStore();

  return useMutation({
    mutationFn: logout,
    onSuccess: () => {
      setUserLogout();
      window.localStorage.removeItem('accessToken');
      window.sessionStorage.removeItem('accessToken');
      navigate('/login');
    },
  });
};

export { useGetRole, useLogin, useLogout };
