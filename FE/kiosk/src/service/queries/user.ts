import { OrderRequest } from '@/types/order';
import { useMutation } from '@tanstack/react-query';
import { postOrder } from '@/service/apis/order';
import { parseState } from '@/utils/parseState';
import useOrderStore from '@/stores/useOrderStore';
import { gcpTts } from '@/service/apis/voice';
import { login, logout, refresh } from '@/service/apis/user';
import { useNavigate } from 'react-router-dom';

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
      navigate('/kiosk');
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
