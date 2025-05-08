export enum Role {
  SUPER = 'SUPER',
  STORE = 'STORE',
}

interface User {
  userId: number;
  role: Role;
}

interface StoreUser extends User {
  role: Role.STORE;
  storeId: number;
  storeName: string;
}

interface AdminUser extends User {
  role: Role.SUPER;
  adminId: number;
  adminName: string;
}

export type { User, StoreUser, AdminUser };
