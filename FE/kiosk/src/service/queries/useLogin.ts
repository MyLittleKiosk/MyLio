import { useMutation } from '@tanstack/react-query';
import { login } from '../apis/user';
import { useNavigate } from 'react-router-dom';

export function useLogin() {
  const navigate = useNavigate();
  return useMutation({
    mutationFn: ({
      email,
      password,
      kioskId,
    }: {
      email: string;
      password: string;
      kioskId: number;
    }) => login(email, password, kioskId),
    onSuccess: () => {
      navigate('/kiosk');
    },
    onError: (error) => {
      alert(error.message);
    },
  });
}
