import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { useClient } from '@/components/contexts/AuthContext';

export default function useCategories(): UseQueryResult<
  AxiosResponse<any>,
  AxiosError<{ message: string }>
> {
  const client = useClient();
  const getCategories = () => {
    return client.get(`/categories/`);
  };

  return useQuery({
    queryKey: ['categories'],
    queryFn: getCategories,
  });
}
