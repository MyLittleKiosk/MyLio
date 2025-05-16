import {
  useMutation,
  useQueryClient,
  useSuspenseQuery,
} from '@tanstack/react-query';
import {
  addKiosk,
  deleteKiosk,
  getKioskDetail,
  getKioskList,
  updateKiosk,
} from '@/service/apis/kiosk';

export const useGetKioskList = (keyword?: string, page?: number) => {
  const query = useSuspenseQuery({
    queryKey: ['kioskList', keyword, page],
    queryFn: () => getKioskList(keyword, page),
  });

  return {
    data: query.data?.data.content,
  };
};

export const useAddKiosk = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ name, startOrder }: { name: string; startOrder: string }) =>
      addKiosk(name, startOrder),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['kioskList'] });
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

export const useGetKioskDetail = (kioskId: number) => {
  const query = useSuspenseQuery({
    queryKey: ['kioskDetail', kioskId],
    queryFn: () => getKioskDetail(kioskId),
  });

  return {
    data: query.data?.data,
  };
};

export const useDeleteKiosk = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (kioskId: number) => deleteKiosk(kioskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['kioskList'] });
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};

export const useUpdateKiosk = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      kioskId,
      name,
      startOrder,
    }: {
      kioskId: number;
      name: string;
      startOrder: string;
    }) => updateKiosk(kioskId, name, startOrder),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['kioskList'] });
    },
    onError: (error) => {
      if (error instanceof Error) {
        alert(error.message);
      }
    },
  });
};
