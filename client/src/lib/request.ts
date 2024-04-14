import axios from 'axios';

import { BACKEND_API_URL } from './constants';

// eslint-disable-next-line import/prefer-default-export
export const axiosUnauthorizedInstance = axios.create({
  baseURL: BACKEND_API_URL,
  headers: {
    'Content-type': 'application/json',
  },
});
