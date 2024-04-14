import {
  useMutation,
  UseMutationResult,
  useQueryClient,
} from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { useClient } from '@/components/contexts/AuthContext';

export default function useCreatePayment(): UseMutationResult<
  AxiosResponse<any>,
  AxiosError<{ message: string }>,
  any
> {
  const client = useClient();
  const queryClient = useQueryClient();

  const postPayment = (payload: any) => {
    return client.post(`payments/`, payload);
  };

  return useMutation({
    mutationKey: ['userProfile'],
    mutationFn: postPayment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['userProfile'] });
    },
  });
}
