import { useMutation } from '@tanstack/react-query';
import { login } from '@/service/apis/user';
import { useNavigate } from 'react-router-dom';

export function useLogin() {
  const navigate = useNavigate();
  return useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      login(email, password),
    onSuccess: () => {
      navigate('/');
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
}
