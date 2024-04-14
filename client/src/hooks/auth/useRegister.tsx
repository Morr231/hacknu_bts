import { useMutation, UseMutationResult } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { axiosUnauthorizedInstance } from '@/lib/request';

export default function useRegister(): UseMutationResult<
  AxiosResponse<any>,
  AxiosError<{ message: string }>,
  any
> {
  const register = (payload: any) => {
    return axiosUnauthorizedInstance.post('auth/register', payload);
  };
  return useMutation({
    mutationKey: ['register'],
    mutationFn: register,
  });
}
