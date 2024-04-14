import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { useClient } from '@/components/contexts/AuthContext';

export default function usePartners(
  partner_id: string
): UseQueryResult<
  AxiosResponse<any>,
  AxiosError<{ message: string }>
> {
  const client = useClient();
  const getPartners = () => {
    return client.get(`offers/partners`, {
      params: {
        partner_id,
      },
    });
  };

  return useQuery({
    queryKey: ['partners', partner_id],
    queryFn: getPartners,
  });
}
