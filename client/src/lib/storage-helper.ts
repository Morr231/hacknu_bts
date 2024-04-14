const TOKEN = {
  ACCESS: 'access_token',
  REFRESH: 'refresh_token',
};

export const clearTokens = () => {
  localStorage.removeItem(TOKEN.ACCESS);
  localStorage.removeItem(TOKEN.REFRESH);
};

export const setTokens = ({
  access,
  refresh,
}: {
  access: string;
  refresh: string;
}) => {
  localStorage.setItem(TOKEN.ACCESS, access);
  localStorage.setItem(TOKEN.REFRESH, refresh);
};

export const getTokens = (): {
  access: string | null;
  refresh: string | null;
} => {
  const access = localStorage.getItem(TOKEN.ACCESS);
  const refresh = localStorage.getItem(TOKEN.REFRESH);

  return {
    access,
    refresh,
  };
};
