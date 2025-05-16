import { getOrders } from '@/service/apis/orders';
import { useSuspenseQuery } from '@tanstack/react-query';

export function useGetOrders(
  startDate?: string,
  endDate?: string,
  page?: number
) {
  const query = useSuspenseQuery({
    queryKey: ['orders', startDate, endDate, page],
    queryFn: () => getOrders(startDate, endDate, page),
    refetchOnWindowFocus: false,
    // placeholderData: (previousData) => previousData,
  });

  const pageInfo = {
    first: query.data?.data.first,
    last: query.data?.data.last,
    pageNumber: query.data?.data.pageNumber,
    pageSize: query.data?.data.pageSize,
    totalElements: query.data?.data.totalElements,
    totalPages: query.data?.data.totalPages,
  };

  return {
    data: query.data?.data.content,
    isLoading: query.isLoading,
    isError: query.isError,
    pageInfo,
  };
}
