interface Response<T> {
  success: boolean;
  data: T;
  error: string | null;
  timestamp: string;
}

type CustomError = Error & {
  response: { data: { error: { message: string } } };
};

export type { Response, CustomError };
