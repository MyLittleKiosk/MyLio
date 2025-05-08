import { useQuery } from '@tanstack/react-query';

import getMenus from '@/service/apis/menu';

import { MenuType } from '@/types/menus';
import { PaginationResponse, Response } from '@/types/apiResponse';

const useGetMenus = () => {
  const query = useQuery<Response<PaginationResponse<MenuType>>>({
    queryKey: ['menus'],
    queryFn: getMenus,
  });

  return {
    data: query.data?.data.content,
    isLoading: query.isLoading,
    isError: query.isError,
  };
};

export default useGetMenus;
