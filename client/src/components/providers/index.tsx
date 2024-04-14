import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RecoilRoot } from 'recoil';

import { AuthProvider } from '../contexts/AuthContext';
import { ThemeProvider } from '@/components/providers/theme-provider';
import { APP_NAME } from '@/lib/constants';
import { ChildrenProps } from '@/types/globals';

const queryClient = new QueryClient();

function providers({ children }: ChildrenProps) {
  return (
    <RecoilRoot>
      <ThemeProvider defaultTheme='system' storageKey={`${APP_NAME}-ui-theme`}>
        <QueryClientProvider client={queryClient}>
          <AuthProvider>{children}</AuthProvider>
        </QueryClientProvider>
      </ThemeProvider>
    </RecoilRoot>
  );
}

export default providers;
