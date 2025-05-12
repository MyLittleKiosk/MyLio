import { OrderRequest } from '@/types/order';
import { useMutation } from '@tanstack/react-query';
import { postOrder } from '@/service/apis/order';
import { parseState } from '@/utils/parseState';
import { useNavigate } from 'react-router-dom';
import useOrderStore from '@/stores/useOrderStore';
import { gcpTts } from '@/service/apis/voice';
export function useOrderRequest() {
  const { setOrder } = useOrderStore();
  const navigate = useNavigate();
  return useMutation({
    mutationFn: (order: OrderRequest) => postOrder(order),
    onSuccess: async (data) => {
      const state = data.data.screenState;
      setOrder(data.data);
      if (data.data.reply) {
        const voice = await gcpTts(data.data.reply);
        const audio = new Audio(URL.createObjectURL(voice));
        audio.play();
      }
      navigate(`/kiosk${parseState(state)}`);
    },
  });
}
