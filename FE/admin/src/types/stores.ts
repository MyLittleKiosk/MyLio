interface Store {
  store_id: number;
  store_name: string;
  address: string;
}

interface StoreList {
  stores: Store[];
}

export type { Store, StoreList };
