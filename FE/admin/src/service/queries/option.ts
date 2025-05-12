import { QueryClient, useMutation, useQuery } from '@tanstack/react-query';
import { OptionList } from '@/types/options';
import {
  addOptionDetail,
  addOptionGroup,
  deleteOptionDetail,
  deleteOptionGroup,
  editOptionDetail,
  editOptionGroup,
  getOptions,
} from '@/service/apis/option';
import useModalStore from '@/stores/useModalStore';

const useGetOptions = () => {
  const query = useQuery<OptionList>({
    queryKey: ['options'],
    queryFn: getOptions,
  });

  return {
    data: query.data?.data.options,
    isLoading: query.isLoading,
    isError: query.isError,
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
    }) => editOptionGroup({ optionId, optionNameKr, optionNameEn }),
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
    mutationFn: ({ optionId }: { optionId: number }) =>
      deleteOptionGroup({ optionId }),
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
const useAddOptionDetail = () => {
  return useMutation({
    mutationFn: ({
      optionId,
      value,
      additionalPrice,
    }: {
      optionId: number;
      value: string;
      additionalPrice: number;
    }) => addOptionDetail({ optionId, value, additionalPrice }),
    onSuccess: () => {},
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

const useEditOptionDetail = () => {
  return useMutation({
    mutationFn: ({
      optionDetailId,
      value,
      additionalPrice,
    }: {
      optionDetailId: number;
      value: string;
      additionalPrice: number;
    }) => editOptionDetail({ optionDetailId, value, additionalPrice }),
    onSuccess: () => {},
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

const useDeleteOptionDetail = () => {
  return useMutation({
    mutationFn: ({ optionDetailId }: { optionDetailId: number }) =>
      deleteOptionDetail({ optionDetailId }),
    onSuccess: () => {},
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
  useAddOptionDetail,
  useEditOptionDetail,
  useDeleteOptionDetail,
};
