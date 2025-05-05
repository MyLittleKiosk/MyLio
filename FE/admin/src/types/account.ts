interface Account {
  account_id: number;
  user_name: string;
  email: string;
  store_name: string;
  address: string;
}

interface AccountPagenation {
  accounts: Account[];
  page_number: number;
  total_pages: number;
  total_elements: number;
  page_size: number;
  first: boolean;
  last: boolean;
}

interface AccountForm {
  user_name: string;
  email: string;
  store_name: string;
  address: string;
}

export type { Account, AccountForm, AccountPagenation };
