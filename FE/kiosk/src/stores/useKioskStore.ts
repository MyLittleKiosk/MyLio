import { create } from 'zustand';

interface KioskStore {
  kioskId: number;
  setKioskId: (kioskId: number) => void;
}

const useKioskStore = create<KioskStore>((set) => ({
  kioskId: 0,
  setKioskId: (kioskId: number) => set({ kioskId }),
}));

export default useKioskStore;
