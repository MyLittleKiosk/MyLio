import { create } from 'zustand';

interface KioskStore {
  kioskId: string;
  orderId: number;
  isMute: boolean;
  setKioskId: (kioskId: string) => void;
  setOrderId: (orderId: number) => void;
  increaseOrderId: () => void;
  setIsMute: (isMute: boolean) => void;
}

const useKioskStore = create<KioskStore>((set) => ({
  kioskId: 'A',
  orderId: 0,
  isMute: false,
  setKioskId: (kioskId: string) => set({ kioskId }),
  setOrderId: (orderId: number) => set({ orderId }),
  increaseOrderId: () => set((state) => ({ orderId: state.orderId + 1 })),
  setIsMute: (isMute: boolean) => set({ isMute }),
}));

export default useKioskStore;
