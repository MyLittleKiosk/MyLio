interface User {
  userId: number;
  role: 'SUPER' | 'STORE';
}

interface StoreUser extends User {
  storeId: number;
  storeName: string;
}

interface AdminUser extends User {
  adminId: number;
  adminName: string;
}
