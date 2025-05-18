import {
  QueryClient,
  useMutation,
  useQuery,
  useSuspenseQuery,
} from '@tanstack/react-query';
import { OptionGroup } from '@/types/options';
import {
  addOptionDetail,
  addOptionGroup,
  deleteOptionDetail,
  deleteOptionGroup,
  editOptionDetail,
  editOptionGroup,
  getOptionDetail,
  getOptions,
} from '@/service/apis/option';
import useModalStore from '@/stores/useModalStore';
import { PaginationResponse, Response } from '@/types/apiResponse';

const useGetOptions = (keyword?: string, page?: number) => {
  const query = useSuspenseQuery<Response<PaginationResponse<OptionGroup>>>({
    queryKey: ['options', keyword, page],
    queryFn: () => getOptions(keyword, page),
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

const useAddOptionGroup = () => {
  const queryClient = new QueryClient();
  const { closeModal } = useModalStore();

  return useMutation({
    mutationFn: ({
      optionNameKr,
      optionNameEn,
    }: {
      optionNameKr: string;
      optionNameEn: string;
    }) => addOptionGroup({ optionNameKr, optionNameEn }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['options'] });
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

const useEditOptionGroup = () => {
  const queryClient = new QueryClient();

  return useMutation({
    mutationFn: ({
      optionId,
      optionNameKr,
      optionNameEn,
    }: {
      optionId: number;
      optionNameKr: string;
      optionNameEn: string;
    }) => editOptionGroup(optionId, optionNameKr, optionNameEn),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['options'] });
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

const useDeleteOptionGroup = () => {
  const queryClient = new QueryClient();

  return useMutation({
    mutationFn: (optionId: number) => deleteOptionGroup(optionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['options'] });
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

const useGetOptionDetail = (optionId: number) => {
  const query = useQuery({
    queryKey: ['optionDetail', optionId],
    queryFn: () => getOptionDetail(optionId),
  });

  return {
    data: query.data?.data?.optionDetails,
    isLoading: query.isLoading,
    isError: query.isError,
  };
};

const useAddOptionDetail = () => {
  const queryClient = new QueryClient();

  return useMutation({
    mutationFn: ({
      optionId,
      value,
      additionalPrice,
    }: {
      optionId: number;
      value: string;
      additionalPrice: number;
    }) => addOptionDetail(optionId, value, additionalPrice),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['optionDetail'] });
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

const useEditOptionDetail = () => {
  const queryClient = new QueryClient();

  return useMutation({
    mutationFn: ({
      optionDetailId,
      value,
      additionalPrice,
    }: {
      optionDetailId: number;
      value: string;
      additionalPrice: number;
    }) => editOptionDetail(optionDetailId, value, additionalPrice),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['optionDetail'] });
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

const useDeleteOptionDetail = () => {
  const queryClient = new QueryClient();

  return useMutation({
    mutationFn: (optionDetailId: number) => deleteOptionDetail(optionDetailId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['optionDetail'] });
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

export {
  useGetOptions,
  useAddOptionGroup,
  useEditOptionGroup,
  useDeleteOptionGroup,
  useGetOptionDetail,
  useAddOptionDetail,
  useEditOptionDetail,
  useDeleteOptionDetail,
};
