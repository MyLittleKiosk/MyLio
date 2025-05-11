import { useQuery } from '@tanstack/react-query';

import getMenus from '@/service/apis/menu';

import { MenuType } from '@/types/menus';
import { PaginationResponse, Response } from '@/types/apiResponse';

const useGetMenus = (page?: number, categoryId?: number) => {
  const query = useQuery<Response<PaginationResponse<MenuType>>>({
    queryKey: ['menus', page, categoryId],
    queryFn: () => getMenus(page, categoryId),
  });

  return {
    data: query.data?.data.content,
    isLoading: query.isLoading,
    isError: query.isError,
  };
};

export default useGetMenus;
