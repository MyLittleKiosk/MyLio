import { create } from 'zustand';

interface KioskStore {
  kioskId: string;
  orderId: number;
  setKioskId: (kioskId: string) => void;
  setOrderId: (orderId: number) => void;
  increaseOrderId: () => void;
}

const useKioskStore = create<KioskStore>((set) => ({
  kioskId: 'A',
  orderId: 0,
  setKioskId: (kioskId: string) => set({ kioskId }),
  setOrderId: (orderId: number) => set({ orderId }),
  increaseOrderId: () => set((state) => ({ orderId: state.orderId + 1 })),
}));

export default useKioskStore;
