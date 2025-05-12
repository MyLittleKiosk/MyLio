import { OrderResponse } from '@/types/order';
import { create } from 'zustand';
interface OrderStore {
  order: OrderResponse;
  setOrder: (order: OrderResponse) => void;
  resetOrder: () => void;
}
const useOrderStore = create<OrderStore>((set) => ({
  order: {
    preText: null,
    postText: null,
    reply: null,
    screenState: 'MAIN',
    language: 'KR',
    sessionId: null,
    cart: [],
    contents: [],
    payment: null,
    storeId: null,
  },
  setOrder: (order: OrderResponse) => set({ order }),
  resetOrder: () =>
    set({
      order: {
        preText: null,
        postText: null,
        reply: null,
        screenState: 'MAIN',
        language: 'KR',
        sessionId: null,
        cart: [],
        contents: [],
        payment: null,
        storeId: null,
      },
    }),
}));

export default useOrderStore;
