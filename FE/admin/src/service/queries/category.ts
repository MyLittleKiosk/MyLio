import { useQuery } from '@tanstack/react-query';

import { PaginationResponse, Response } from '@/types/apiResponse';
import { CategoryType } from '@/types/categories';

import { getCategory } from '@/service/apis/category';

const useGetCategory = (page?: number) => {
  const query = useQuery<Response<PaginationResponse<CategoryType>>>({
    queryKey: ['category', page],
    queryFn: () => getCategory(page),
  });

  return {
    data: query.data?.data.content,
    isLoading: query.isLoading,
    isError: query.isError,
  };
};

export default useGetCategory;
