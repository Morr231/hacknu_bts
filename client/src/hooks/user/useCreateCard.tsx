import {
  useMutation,
  UseMutationResult,
  useQueryClient,
} from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { useClient } from '@/components/contexts/AuthContext';

export default function useCreateCard(): UseMutationResult<
  AxiosResponse<any>,
  AxiosError<{ message: string }>,
  any
> {
  const client = useClient();
  const queryClient = useQueryClient();

  const postCard = (payload: any) => {
    return client.post(`cards`, payload);
  };

  return useMutation({
    mutationKey: ['userProfile'],
    mutationFn: postCard,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['userProfile'] });
    },
  });
}
