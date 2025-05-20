import { parseState } from '@/utils/parseState';
import { useMutation } from '@tanstack/react-query';
import { OrderRequest } from '@/types/order';
import { useNavigate } from 'react-router-dom';
import { postOrder, postSuccess, requestPay } from '@/service/apis/order';
import useOrderStore from '@/stores/useOrderStore';
import { PayRequest } from '@/types/kakaoPay';

export function useOrderRequest() {
  const { setOrder } = useOrderStore();
  const navigate = useNavigate();
  return useMutation({
    mutationFn: (order: OrderRequest) => postOrder(order),
    onSuccess: async (data) => {
      const state = data.data.screenState;
      setOrder(data.data);
      navigate(`/kiosk${parseState(state)}`);
    },
  });
}

export function useRequestPay() {
  const { order } = useOrderStore();
  return useMutation({
    mutationFn: (payRequest: PayRequest) => requestPay(payRequest),
    onSuccess: (data) => {
      sessionStorage.setItem('cartItem', JSON.stringify(order.cart));
      return data;
    },
    onError: (error) => {
      console.error('결제 중 오류 발생:', error);
    },
  });
}

export function usePostSuccess() {
  const navigate = useNavigate();
  return useMutation({
    mutationFn: ({
      orderId,
      pgToken,
    }: {
      orderId: string;
      pgToken: string;
    }) => {
      return postSuccess({
        orderId,
        pgToken,
        cart: JSON.parse(sessionStorage.getItem('cartItem') || '[]'),
      });
    },
    onSuccess: () => {
      sessionStorage.removeItem('cartItem');
      navigate('/success');
    },
    onError: (error) => {
      console.error('결제 성공 중 오류 발생:', error);
      navigate('/kiosk/select-pay');
    },
  });
}
