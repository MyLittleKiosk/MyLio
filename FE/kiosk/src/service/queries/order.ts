import { parseState } from '@/utils/parseState';
import { gcpTts } from '@/service/apis/voice';
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
      try {
        navigate(`/kiosk${parseState(state)}`);
        if (data.data.reply) {
          const voice = await gcpTts(data.data.reply);
          const audio = new Audio(URL.createObjectURL(voice));
          audio.play();
        }
      } catch (error) {
        console.error('음성 출력 중 오류 발생:', error);
      }
    },
  });
}

export function useRequestPay() {
  return useMutation({
    mutationFn: (payRequest: PayRequest) => requestPay(payRequest),
    onSuccess: (data) => {
      window.location.href = data.data.next_redirect_pc_url;
    },
    onError: (error) => {
      console.error('결제 중 오류 발생:', error);
    },
  });
}

export function usePostSuccess() {
  const { order } = useOrderStore();
  const navigate = useNavigate();
  return useMutation({
    mutationFn: ({
      orderId,
      pgToken,
    }: {
      orderId: string;
      pgToken: string;
    }) => {
      return postSuccess({ orderId, pgToken, cart: order.cart });
    },
    onSuccess: () => {
      alert('결제 성공');
      navigate('/kiosk/pay/success');
    },
    onError: (error) => {
      console.error('결제 성공 중 오류 발생:', error);
      navigate('/kiosk/select-pay');
    },
  });
}
