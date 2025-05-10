import { useMutation, useQuery } from '@tanstack/react-query';
import { OptionList } from '@/types/options';
import {
  addOptionDetail,
  addOptionGroup,
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

const useAddOptionDetail = () => {
  const { closeModal } = useModalStore();

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

export { useGetOptions, useAddOptionGroup, useAddOptionDetail };
