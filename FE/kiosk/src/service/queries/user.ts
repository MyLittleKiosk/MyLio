import { login, logout, refresh } from '@/service/apis/user';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';

export function useLogout() {
  const navigate = useNavigate();
  const kioskId = Number(localStorage.getItem('kioskId'));
  return useMutation({
    mutationFn: () => logout(kioskId),
    onSuccess: () => {
      localStorage.removeItem('kioskId');
      navigate('/');
    },
  });
}

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
    onSuccess: ({ data }) => {
      localStorage.setItem('kioskId', data.kioskId.toString());
      sessionStorage.setItem('orderCount', '1');
      navigate('/landing');
    },
    onError: (error) => {
      alert(error.message);
    },
  });
}

export function useRefresh() {
  return useMutation({
    mutationFn: refresh,
  });
}
