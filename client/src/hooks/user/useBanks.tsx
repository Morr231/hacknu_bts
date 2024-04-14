import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { useClient } from '@/components/contexts/AuthContext';

export default function useBanks(): UseQueryResult<
  AxiosResponse<any>,
  AxiosError<{ message: string }>
> {
  const client = useClient();

  const getBanks = () => {
    return client.get(`banks`);
  };

  return useQuery({
    queryKey: ['banks'],
    queryFn: getBanks,
  });
}
