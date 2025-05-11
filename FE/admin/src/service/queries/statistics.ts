import {
  getSalesTrend,
  getStatisticsByCategory,
  getStatisticsByDaily,
  getStatisticsByOrder,
  getStatisticsByPayment,
} from '@/service/apis/statistics';
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

function useGetStatisticsByCategory(year: number, month?: number) {
  const query = useQuery({
    queryKey: ['statisticsByCategory', year, month],
    queryFn: () => getStatisticsByCategory(year, month),
  });

  return {
    data: query.data?.data,
    isLoading: query.isLoading,
    isError: query.isError,
  };
}

function useGetStatisticsByOrder(year: number, month?: number) {
  const query = useQuery({
    queryKey: ['statisticsByOrder', year, month],
    queryFn: () => getStatisticsByOrder(year, month),
  });

  return {
    data: query.data?.data,
    isLoading: query.isLoading,
    isError: query.isError,
  };
}

function useGetStatisticsByPayment(year: number, month?: number) {
  const query = useQuery({
    queryKey: ['statisticsByPayment', year, month],
    queryFn: () => getStatisticsByPayment(year, month),
  });

  return {
    data: query.data?.data,
    isLoading: query.isLoading,
    isError: query.isError,
  };
}

function useGetStatisticsByDaily() {
  const query = useQuery({
    queryKey: ['statisticsByDaily'],
    queryFn: () => getStatisticsByDaily(),
  });

  return {
    data: query.data?.data,
    isLoading: query.isLoading,
    isError: query.isError,
  };
}

export {
  useGetSalesTrend,
  useGetStatisticsByCategory,
  useGetStatisticsByDaily,
  useGetStatisticsByOrder,
  useGetStatisticsByPayment,
};
