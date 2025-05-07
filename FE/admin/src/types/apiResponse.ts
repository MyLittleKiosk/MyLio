interface Response<T> {
  success: boolean;
  data: T;
  error?: string | null;
  timestamp: string;
}

export type { Response };
