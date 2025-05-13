export interface Response<T> {
  success: boolean;
  data: T;
  error?: string;
  timestamp: string;
}

export type CustomError = Error & {
  response: { data: { error: { message: string } } };
};

export interface PaginationResponse<T> extends Pagenation {
  content: T[];
}

export interface Pagenation {
  pageNumber: number;
  totalPages: number;
  totalElements: number;
  pageSize: number;
  first: boolean;
  last: boolean;
}
