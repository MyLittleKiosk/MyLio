interface Response<T> {
  success: boolean;
  data: T;
  error?: string;
  timestamp: string;
}

export type { Response };
