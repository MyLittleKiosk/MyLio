import {
  getSalesTrend,
  getStatisticsByCategory,
  getStatisticsByDaily,
  getStatisticsByOrder,
  getStatisticsByPayment,
} from '@/service/apis/statistics';
import { useSuspenseQuery } from '@tanstack/react-query';

function useGetSalesTrend(year: number, month?: number) {
  const query = useSuspenseQuery({
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
  const query = useSuspenseQuery({
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
  const query = useSuspenseQuery({
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
  const query = useSuspenseQuery({
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
  const query = useSuspenseQuery({
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
