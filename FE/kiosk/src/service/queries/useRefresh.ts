import { useMutation } from '@tanstack/react-query';
import { refresh } from '../apis/user';

export function useRefresh() {
  return useMutation({
    mutationFn: refresh,
  });
}
