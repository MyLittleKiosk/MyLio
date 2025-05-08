import { getSalesTrend } from '@/service/apis/statistics';
import { useQuery } from '@tanstack/react-query';

function useGetSalesTrend(year: number, month?: number) {
  const query = useQuery({
    queryKey: ['salesTrend', year, month],
    queryFn: () => getSalesTrend(year, month),
  });

  return {
    data: query.data?.data,
    isLoading: query.isLoading,
    isError: query.isError,
  };
}

export default useGetSalesTrend;
