import { create } from 'zustand';

interface OrderCounterStore {
  count: number;
  baseId: string;
  increment: () => void;
  setBaseId: (baseId: string) => void;
}

const counterStore = create<OrderCounterStore>((set) => ({
  count: 0,
  baseId: '',
  increment: () => set((state) => ({ count: state.count + 1 })),
  setBaseId: (baseId: string) => set({ baseId }),
}));

export default counterStore;
