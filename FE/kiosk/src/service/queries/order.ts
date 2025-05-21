import { parseState } from '@/utils/parseState';
import { useMutation } from '@tanstack/react-query';
import { OrderRequest } from '@/types/order';
import { useNavigate } from 'react-router-dom';
import { postOrder, postSuccess, requestPay } from '@/service/apis/order';
import useOrderStore from '@/stores/useOrderStore';
import { PayRequest } from '@/types/kakaoPay';

export function useOrderRequest() {
  const { setOrder, order } = useOrderStore();
  const navigate = useNavigate();
  return useMutation({
    mutationFn: (order: OrderRequest) => postOrder(order),
    onSuccess: async (data) => {
      console.log('Order Request Success:', data);
      const state = data.data.screenState;
      setOrder(data.data);
      console.log('Updated order data:', data.data);
      navigate(`/kiosk${parseState(state)}`);
    },
    onError: (error) => {
      console.error('Order Request Error:', error);
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
  const { resetOrder } = useOrderStore();
  const navigate = useNavigate();
  return useMutation({
    mutationFn: ({
      orderId,
      pgToken,
      payMethod,
    }: {
      orderId: string;
      pgToken: string | null;
      payMethod: string;
    }) => {
      return postSuccess(
        {
          orderId,
          pgToken: pgToken || null,
          cart: JSON.parse(sessionStorage.getItem('cartItem') || '[]'),
        },
        payMethod
      );
    },
    onSuccess: () => {
      sessionStorage.removeItem('cartItem');
      resetOrder();
      navigate('/success');
    },
    onError: (error) => {
      console.error('결제 성공 중 오류 발생:', error);
      navigate('/kiosk/select-pay');
    },
  });
}
