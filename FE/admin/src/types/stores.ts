interface StoreType {
  store_id: number;
  store_name: string;
  address: string;
}

interface StoreList {
  stores: StoreType[];
}

export type { StoreType, StoreList };
