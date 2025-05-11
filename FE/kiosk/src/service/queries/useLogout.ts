import { useMutation } from '@tanstack/react-query';
import { logout } from '../apis/user';

export function useLogout() {
  return useMutation({
    mutationFn: (kioskId: number) => logout(kioskId),
  });
}
