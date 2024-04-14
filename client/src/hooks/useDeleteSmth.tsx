import { useMutation, UseMutationResult } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { axiosUnauthorizedInstance } from '@/lib/request';

export default function useDeleteSmth(): UseMutationResult<
  AxiosResponse<void>,
  AxiosError<{ message: string }>,
  string
> {
  const deleteSmth = (SmthId: string) => {
    return axiosUnauthorizedInstance.delete(`/smth/${SmthId}/`);
  };

  return useMutation({
    mutationKey: ['smth'],
    mutationFn: deleteSmth,
  });
}
