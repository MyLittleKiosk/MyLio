import {
  useMutation,
  useQueryClient,
  useSuspenseQuery,
} from '@tanstack/react-query';
import {
  getNutritionList,
  addNutritionTemplate,
  patchNutritionTemplate,
} from '../apis/nutrient';
import { NutritionTemplateAddType } from '@/types/nutrient';

export const useGetNutritionList = (keyword?: string, page?: number) => {
  const query = useSuspenseQuery({
    queryKey: ['nutritionList', keyword, page],
    queryFn: () => getNutritionList(keyword, page),
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

export const useAddNutritionTemplate = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (nutrition: NutritionTemplateAddType) =>
      addNutritionTemplate(nutrition),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['nutritionList'] });
    },
    onError: (error: unknown) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

export const usePatchNutritionTemplate = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      nutritionId,
      nutrition,
    }: {
      nutritionId: number;
      nutrition: NutritionTemplateAddType;
    }) => patchNutritionTemplate(nutritionId, nutrition),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['nutritionList'] });
    },
    onError: (error: unknown) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};
