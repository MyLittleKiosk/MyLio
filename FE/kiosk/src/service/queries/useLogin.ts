import { useMutation } from '@tanstack/react-query';
import { login } from '../apis/user';
import { useNavigate } from 'react-router-dom';
import useKioskStore from '@/stores/useKioskStore';

export function useLogin() {
  const navigate = useNavigate();
  const { setKioskId } = useKioskStore();
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
      setKioskId(data.kioskId);
      navigate('/kiosk');
    },
    onError: (error) => {
      alert(error.message);
    },
  });
}
