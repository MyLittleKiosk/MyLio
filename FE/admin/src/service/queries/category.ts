import { useQuery } from '@tanstack/react-query';

import { PaginationResponse, Response } from '@/types/apiResponse';
import { CategoryType } from '@/types/categories';

import { getCategory } from '@/service/apis/category';

const useGetCategory = (pageable: number) => {
  const query = useQuery<Response<PaginationResponse<CategoryType>>>({
    queryKey: ['category', pageable],
    queryFn: () => getCategory(pageable),
  });

  return {
    data: query.data?.data.content,
    isLoading: query.isLoading,
    isError: query.isError,
  };
};

export default useGetCategory;
