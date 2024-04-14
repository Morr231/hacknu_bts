import { useMutation, UseMutationResult } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { useClient } from '@/components/contexts/AuthContext';

export default function useSearch(): UseMutationResult<
  AxiosResponse<any>,
  AxiosError<{ message: string }>,
  any
> {
  const client = useClient();

  const search = (payload: any) => {
    return client.post(`search/partners`, payload);
  };

  return useMutation({
    mutationKey: ['search'],
    mutationFn: search,
  });
}
