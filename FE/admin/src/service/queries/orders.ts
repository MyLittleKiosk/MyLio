import { getOrders } from '@/service/apis/orders';
import { useQuery } from '@tanstack/react-query';

export function useGetOrders(
  startDate?: string,
  endDate?: string,
  pageable?: number
) {
  const query = useQuery({
    queryKey: ['orders', startDate, endDate, pageable],
    queryFn: () => getOrders(startDate, endDate, pageable),
    refetchOnWindowFocus: false,
    placeholderData: (previousData) => previousData,
  });

  return {
    data: query.data?.data.content,
    isLoading: query.isLoading,
    isError: query.isError,
  };
}
