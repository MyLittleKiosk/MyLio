import {
  useMutation,
  useQueryClient,
  useSuspenseQuery,
} from '@tanstack/react-query';

import { PaginationResponse, Response } from '@/types/apiResponse';
import { CategoryType } from '@/types/categories';

import {
  addCategory,
  deleteCategory,
  editCategory,
  getCategory,
} from '@/service/apis/category';
import useModalStore from '@/stores/useModalStore';

export const useGetCategory = (
  keyword?: string,
  page?: number,
  size?: number
) => {
  const query = useSuspenseQuery<Response<PaginationResponse<CategoryType>>>({
    queryKey: ['category', keyword, page, size],
    queryFn: () => getCategory(keyword, page, size),
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

export const useAddCategory = () => {
  const queryClient = useQueryClient();
  const { closeModal } = useModalStore();

  return useMutation({
    mutationFn: ({ nameKr, nameEn }: { nameKr: string; nameEn: string }) =>
      addCategory(nameKr, nameEn),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['category'] });
      alert('등록에 성공했습니다.');
      closeModal();
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

export const useEditCategory = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      categoryId,
      nameKr,
      nameEn,
    }: {
      categoryId: number;
      nameKr: string;
      nameEn: string;
    }) => editCategory(categoryId, nameKr, nameEn),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['category'] });
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

export const useDeleteCategory = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (categoryId: number) => deleteCategory(categoryId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['category'] });
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      } else {
        alert('알 수 없는 오류가 발생했습니다.');
      }
    },
  });
};
