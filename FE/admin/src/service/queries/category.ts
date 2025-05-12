import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { PaginationResponse, Response } from '@/types/apiResponse';
import { CategoryType } from '@/types/categories';

import {
  addCategory,
  editCategory,
  getCategory,
} from '@/service/apis/category';
import useModalStore from '@/stores/useModalStore';

export const useGetCategory = (page?: number) => {
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
