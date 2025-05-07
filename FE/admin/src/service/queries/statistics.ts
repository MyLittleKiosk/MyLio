import { getSalesTrend } from '@/service/apis/statistics';
import { useQuery } from '@tanstack/react-query';

export const useGetSalesTrend = (year: number, month?: number) => {
  return useQuery({
    queryKey: ['salesTrend', year, month],
    queryFn: () => getSalesTrend(year, month),
  });
};
