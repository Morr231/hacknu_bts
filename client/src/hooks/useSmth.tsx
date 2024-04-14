import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { axiosUnauthorizedInstance } from '@/lib/request';

export default function useSmth(): UseQueryResult<
  AxiosResponse<any[]>,
  AxiosError<{ message: string }>
> {
  const getSmth = () => {
    return axiosUnauthorizedInstance.get(`/smth`);
  };

  return useQuery({
    queryKey: ['smth'],
    queryFn: getSmth,
  });
}
