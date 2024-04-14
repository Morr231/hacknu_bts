import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { axiosUnauthorizedInstance } from '@/lib/request';

export default function useCities(): UseQueryResult<
  AxiosResponse<any>,
  AxiosError<{ message: string }>
> {
  const getCities = () => {
    return axiosUnauthorizedInstance.get(`cities`);
  };

  return useQuery({
    queryKey: ['cities'],
    queryFn: getCities,
  });
}
