import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { AxiosError, AxiosResponse } from 'axios';

import { useClient } from '@/components/contexts/AuthContext';

export default function useUserProfile({
  enabled,
  token,
}: {
  enabled: boolean;
  token: any;
}): UseQueryResult<AxiosResponse<any>, AxiosError<{ message: string }>> {
  const client = useClient();

  const getUserProfile = () => {
    return client.get(`users/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
  };

  return useQuery({
    queryKey: ['userProfile'],
    queryFn: getUserProfile,
    enabled,
  });
}
