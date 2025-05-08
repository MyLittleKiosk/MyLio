import authClient from '@/service/authClient';
import { Response } from '@/types/apiResponse';
import { SalesTrendType } from '@/types/statistics';

export async function getSalesTrend(
  year: number,
  month?: number
): Promise<Response<SalesTrendType[]>> {
  try {
    const params = month ? { year, month } : { year };
    const res = await authClient.get('/sales', {
      params,
    });
    return res.data;
  } catch (e: unknown) {
    if (e instanceof Error) throw new Error(e.message);
    else throw new Error('unknown Error');
  }
}
