export interface Response<T> {
  success: boolean;
  data: T;
  error?: string;
  timestamp: string;
}

export interface PaginationResponse<T> {
  content: T[];
  page_number: number;
  total_pages: number;
  total_elements: number;
  page_size: number;
  first: boolean;
  last: boolean;
}
