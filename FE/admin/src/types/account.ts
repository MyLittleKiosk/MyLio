export type AccountType = {
  accountId: number;
  userName: string;
  email: string;
  storeName: string;
  address: string;
};

export interface AccountForm {
  userName: string;
  email: string;
  storeName: string;
  address: string;
}
