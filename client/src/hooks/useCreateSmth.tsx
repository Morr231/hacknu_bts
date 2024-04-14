import { useMutation, UseMutationResult } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { axiosUnauthorizedInstance } from '@/lib/request';

export default function useCreateSmth(): UseMutationResult<
  AxiosResponse<any>,
  AxiosError<{ message: string }>,
  any
> {
  const postSmth = (payload: any) => {
    return axiosUnauthorizedInstance.post(`/smth/`, payload);
  };

  return useMutation({
    mutationKey: ['smth'],
    mutationFn: postSmth,
  });
}
