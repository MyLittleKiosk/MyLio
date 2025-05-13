import { useMutation } from '@tanstack/react-query';
import { logout } from '../apis/user';
import { useNavigate } from 'react-router-dom';

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
