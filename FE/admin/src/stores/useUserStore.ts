import { User } from '@/types/user';
import { create } from 'zustand';

interface UserState {
  user: User | null;
  setUser: (user: User) => void;
  logout: () => void;
}

const useUserStore = create<UserState>((set) => ({
  user: null,
  setUser: (user) => set({ user: user }),
  logout: () => set({ user: null }),
}));

export { useUserStore };
