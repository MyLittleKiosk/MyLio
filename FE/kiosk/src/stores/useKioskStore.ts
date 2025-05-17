import { create } from 'zustand';

interface KioskStore {
  kioskId: number;
  orderId: number;
  setKioskId: (kioskId: number) => void;
  setOrderId: (orderId: number) => void;
}

const useKioskStore = create<KioskStore>((set) => ({
  kioskId: 0,
  orderId: 1,
  setKioskId: (kioskId: number) => set({ kioskId }),
  setOrderId: (orderId: number) => set({ orderId }),
}));

export default useKioskStore;
