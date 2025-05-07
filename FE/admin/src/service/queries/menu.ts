import { useQuery } from '@tanstack/react-query';
import getMenus from '../apis/menu';
import { MenuList } from '@/types/menus';
import { Response } from '@/types/apiResponse';

const useGetMenus = () => {
  const query = useQuery<Response<MenuList>>({
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
