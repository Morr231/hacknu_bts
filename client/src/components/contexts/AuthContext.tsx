import { createContext, useCallback, useContext, useState } from 'react';

import axios from 'axios';

import useLogin from '@/hooks/auth/useLogin';
import useRegister from '@/hooks/auth/useRegister';
import useUserProfile from '@/hooks/user/useUserProfile';
import { BACKEND_API_URL } from '@/lib/constants';
import { axiosUnauthorizedInstance } from '@/lib/request';
import { clearTokens, getTokens, setTokens } from '@/lib/storage-helper';

const AuthContext = createContext({});

function AuthProvider(props: any): JSX.Element {
  const loginMutation = useLogin();
  const registerMutation = useRegister();

  const { access: initialAccessToken } = getTokens();
  const [token, setToken] = useState(initialAccessToken);

  const handleSetTokens = ({
    access,
    refresh,
  }: {
    access: string;
    refresh: string;
  }): void => {
    setToken(access);
    setTokens({ access, refresh });
  };

  const handleLogin = (payload: any) => {
    loginMutation.mutate(payload, {
      onSuccess: (response) => {
        handleSetTokens({
          access: response.data.access_token,
          refresh: response.data.refresh_token,
        });
        window.location.replace('/');
      },
      onError: () => {
        console.log('Hello');
      },
    });
  };

  const handleRegister = (payload: any): void => {
    registerMutation.mutate(payload, {
      onSuccess: () => {
        handleLogin({
          username: payload.email,
          password: payload.password,
        });
      },
      onError: () => {
        console.log('hello');
      },
    });
  };

  const {
    data: userProfileData,
    isLoading: isUserProfileLoading,
    isSuccess: isUserProfileSuccess,
  } = useUserProfile({
    enabled: !!token,
    token,
  });

  const logout = () => {
    clearTokens();
    setToken(null);
    window.location.replace('/');
  };

  return (
    <AuthContext.Provider
      value={{
        logout,
        setToken,
        handleLogin,
        handleRegister,
        profile: userProfileData?.data,
        isAuthenticated: !!token && isUserProfileSuccess,
        isLoginLoading: loginMutation.isPending || registerMutation.isPending,
        isLoading: isUserProfileLoading,
      }}
      {...props}
    />
  );
}

function useAuth(): any {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error(`useAuth must be used within a AuthProvider`);
  }
  return context;
}

function useClient() {
  const { access: accessToken, refresh: refreshToken } = getTokens();

  return useCallback(() => {
    const cl = axios.create({
      baseURL: BACKEND_API_URL,
    });

    cl.interceptors.request.use((config) => {
      config.headers.set(
        'Authorization',
        accessToken ? `Bearer ${accessToken}` : null,
      );

      return config;
    });

    cl.interceptors.response.use(
      (response) => response,
      async (error) => {
        const conf = error.config;
        if (
          error.responce &&
          error.response.status === 401 &&
          !conf.token_retry
        ) {
          conf.token_retry = true;

          return axiosUnauthorizedInstance
            .post('/auth/refresh-token', { refreshToken })
            .then((res: any) => {
              const access = res.data.access_token;
              const refresh = res.data.refresh_token;

              setTokens({ access, refresh });

              cl.defaults.headers.common.Authorization = `Bearer ${access}`;

              return cl.request(conf);
            })
            .catch((err: any) => {
              clearTokens();
              return Promise.reject(err);
            });
        }

        return Promise.reject(error);
      },
    );

    return cl;
  }, [accessToken])();
}

export { AuthProvider, useAuth, useClient };
