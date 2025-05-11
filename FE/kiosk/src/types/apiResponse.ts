export type ApiResponse<T> = {
  success: boolean;
  data: T;
  error?: string;
  timestamp: string;
};

export type CustomError = Error & {
  response: { data: { error: { message: string } } };
};
