import { getRole, login } from '@/service/apis/user';
import { useUserStore } from '@/stores/useUserStore';
import { Response } from '@/types/apiResponse';
import { User } from '@/types/user';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';

const useLogin = () => {
  const navigate = useNavigate();
  const { setUser } = useUserStore();

  return useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      login(email, password),
    onSuccess: (data: Response<User>) => {
      setUser(data.data);
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
  });

  return {
    data: query.data?.data,
    isLoading: query.isLoading,
    isError: query.error,
  };
};

export { useGetRole, useLogin };
