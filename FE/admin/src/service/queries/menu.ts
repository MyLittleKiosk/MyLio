import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import {
  addMenu,
  getMenuById,
  getMenus,
  updateMenu,
} from '@/service/apis/menu';

import { MenuAdd, MenuDetailGetType, MenuType } from '@/types/menus';
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

export const useGetMenuById = (menuId: number) => {
  const query = useQuery<Response<MenuDetailGetType>>({
    queryKey: ['menuDetail', menuId],
    queryFn: () => getMenuById(menuId),
  });

  return {
    data: query.data?.data,
    isLoading: query.isLoading,
    isError: query.isError,
  };
};

const useAddMenu = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ menu, file }: { menu: MenuAdd; file?: File }) =>
      addMenu(menu, file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['menus'] });
      queryClient.invalidateQueries({ queryKey: ['menuDetail'] });
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

const useUpdateMenu = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      menuId,
      menu,
      file,
    }: {
      menuId: number;
      menu: MenuAdd;
      file?: File;
    }) => updateMenu(menuId, menu, file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['menus'] });
      queryClient.invalidateQueries({ queryKey: ['menuDetail'] });
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

export { useGetMenus, useAddMenu, useUpdateMenu };
