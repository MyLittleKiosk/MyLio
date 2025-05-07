import { client } from '@/service/client';

export async function login(email: string, password: string) {
  try {
    const res = await client.post('/login', { email, password });
    return res.data;
  } catch (error: unknown) {
    if (error instanceof Error) throw new Error(error.message);
    throw new Error('unknown error');
  }
}
