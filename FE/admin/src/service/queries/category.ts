import { useMutation, useQuery } from '@tanstack/react-query';

import { PaginationResponse, Response } from '@/types/apiResponse';
import { CategoryType } from '@/types/categories';

import { getCategory, postCategory } from '@/service/apis/category';
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

export const usePostCategory = () => {
  const { closeModal } = useModalStore();
  return useMutation({
    mutationFn: ({ nameKr, nameEn }: { nameKr: string; nameEn: string }) =>
      postCategory(nameKr, nameEn),
    onSuccess: () => {
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
