import {
  useMutation,
  useQueryClient,
  useSuspenseQuery,
} from '@tanstack/react-query';

import {
  addMenu,
  deleteMenu,
  getMenuById,
  getMenus,
  updateMenu,
} from '@/service/apis/menu';

import { MenuAdd, MenuDetailGetType, MenuType } from '@/types/menus';
import { PaginationResponse, Response } from '@/types/apiResponse';

const useGetMenus = (keyword?: string, page?: number, categoryId?: number) => {
  const query = useSuspenseQuery<Response<PaginationResponse<MenuType>>>({
    queryKey: ['menus', keyword, page, categoryId],
    queryFn: () => getMenus(keyword, page, categoryId),
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
    pageInfo,
  };
};

export const useGetMenuById = (menuId: number) => {
  const query = useSuspenseQuery<Response<MenuDetailGetType>>({
    queryKey: ['menuDetail', menuId],
    queryFn: () => getMenuById(menuId),
  });

  return {
    data: query.data?.data,
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

const useDeleteMenu = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (menuId: number) => deleteMenu(menuId),
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

export { useGetMenus, useAddMenu, useUpdateMenu, useDeleteMenu };
