import { Navigate, Outlet } from 'react-router-dom';

import { useAuth } from './contexts/AuthContext';

const ProtectedRoute = () => {
  const { isAuthenticated } = useAuth();
  console.log(isAuthenticated);

  return isAuthenticated ? <Outlet /> : <Navigate to='/auth/login' />;
};

export default ProtectedRoute;
