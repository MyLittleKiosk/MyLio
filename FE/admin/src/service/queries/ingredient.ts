import {
  getIngredientList,
  patchIngredient,
  postIngredient,
} from '@/service/apis/ingredient';
import { IngredientForm, IngredientType } from '@/types/ingredient';
import { keepPreviousData, useMutation, useQuery } from '@tanstack/react-query';

export const useGetIngredientList = (
  keyword?: string,
  page?: number,
  size?: number
) => {
  const query = useQuery({
    queryKey: ['ingredientList', keyword, page, size],
    queryFn: () => getIngredientList(keyword, page, size),
    placeholderData: keepPreviousData,
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
    isLoading: query.isLoading,
    isError: query.isError,
    pageInfo,
  };
};

export const usePostIngredient = () => {
  const query = useMutation({
    mutationFn: (ingredient: IngredientForm) => postIngredient(ingredient),
  });
  return {
    mutate: query.mutate,
    isPending: query.isPending,
    isError: query.isError,
  };
};

export const usePatchIngredient = () => {
  const query = useMutation({
    mutationFn: (ingredient: IngredientType) => patchIngredient(ingredient),
  });
  return {
    mutate: query.mutate,
    isPending: query.isPending,
    isError: query.isError,
  };
};
