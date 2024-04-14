import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { useClient } from '@/components/contexts/AuthContext';

export default function useCategoryPartners(
  category_id: string
): UseQueryResult<
  AxiosResponse<any>,
  AxiosError<{ message: string }>
> {
  const client = useClient();
  const getCategoryPartners = () => {
    return client.get(`offers/category`, {
      params: {
        category_id,
      },
    });
  };

  return useQuery({
    queryKey: ['category_partners', category_id],
    queryFn: getCategoryPartners,
    enabled: !!category_id,
  });
}
