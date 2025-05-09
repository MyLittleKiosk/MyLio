import { useMutation, useQuery } from '@tanstack/react-query';
import { OptionList } from '@/types/options';
import { addOptionGroup, getOptions } from '@/service/apis/option';

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
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

export { useGetOptions, useAddOptionGroup };
