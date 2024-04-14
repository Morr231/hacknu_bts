import { useMutation, UseMutationResult } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { axiosUnauthorizedInstance } from '@/lib/request';

export default function useLogin(): UseMutationResult<
  AxiosResponse<any>,
  AxiosError<{ message: string }>,
  any
> {
  const login = (payload: any) => {
    const body = new URLSearchParams(payload);

    console.log(body);

    return axiosUnauthorizedInstance.post('auth/access-token', body, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  };
  return useMutation({
    mutationKey: ['login'],
    mutationFn: login,
  });
}
