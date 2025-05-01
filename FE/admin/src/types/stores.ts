interface Store {
  store_id: number;
  store_name: string;
  address: string;
}

interface StoreList {
  success: boolean;
  data: {
    stores: Store[];
  };
  error: string | null;
  timestamp: string;
}

export type { Store, StoreList };
