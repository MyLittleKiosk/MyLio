import { OrderRequest } from '@/types/order';
import { useMutation } from '@tanstack/react-query';
import { postOrder } from '@/service/apis/order';
import { parseState } from '@/utils/parseState';
import { useNavigate } from 'react-router-dom';
import useOrderStore from '@/stores/useOrderStore';
export function useOrderRequest() {
  const { setOrder } = useOrderStore();
  const navigate = useNavigate();
  return useMutation({
    mutationFn: (order: OrderRequest) => postOrder(order),
    onSuccess: (data) => {
      const state = data.data.screenState;
      setOrder(data.data);
      navigate(parseState(state));
    },
  });
}
