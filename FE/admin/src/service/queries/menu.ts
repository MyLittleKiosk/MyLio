import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { addMenu, getMenus } from '@/service/apis/menu';

import { MenuAdd, MenuType } from '@/types/menus';
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

const useAddMenu = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ menu, file }: { menu: MenuAdd; file?: string }) =>
      addMenu(menu, file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['menus'] });
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

export { useGetMenus, useAddMenu };
