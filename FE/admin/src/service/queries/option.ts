import { useQuery } from '@tanstack/react-query';
import { OptionList } from '@/types/options';
import { getOptions } from '@/service/apis/option';

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

export default useGetOptions;
