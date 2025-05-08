export interface Response<T> {
  success: boolean;
  data: T;
  error?: string;
  timestamp: string;
}

export type CustomError = Error & {
  response: { data: { error: { message: string } } };
};

export interface PaginationResponse<T> {
  content: T[];
  pageNumber: number;
  totalPages: number;
  totalElements: number;
  pageSize: number;
  first: boolean;
  last: boolean;
}
