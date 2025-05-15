import { IngredientType } from '@/types/ingredient';
import { useMutation, useQuery } from '@tanstack/react-query';
import {
  getIngredientList,
  patchIngredient,
  postIngredient,
} from '../apis/ingredient';

export const useGetIngredientList = (keyword?: string, page?: number) => {
  const query = useQuery({
    queryKey: ['ingredientList', keyword, page],
    queryFn: () => getIngredientList(keyword, page),
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
    mutationFn: (ingredient: IngredientType) => postIngredient(ingredient),
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
