import { useMutation } from '@tanstack/react-query';
import { login } from '@/service/apis/user';
import { useNavigate } from 'react-router-dom';
import { useUserStore } from '@/stores/useUserStore';
import { User } from '@/types/user';
import { Response } from '@/types/apiResponse';

export function useLogin() {
  const navigate = useNavigate();
  const { setUser } = useUserStore();

  return useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      login(email, password),
    onSuccess: (data: Response<User>) => {
      setUser(data.data);
      navigate('/');
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
}
