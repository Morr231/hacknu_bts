import { BrowserRouter, Routes, Route } from 'react-router-dom';

import { useAuth } from './components/contexts/AuthContext';
import AuthRegister from './pages/AuthRegister';
import Navbar from '@/components/navbar';
import Providers from '@/components/providers';
import AuthLogin from '@/pages/AuthLogin';
import Home from '@/pages/Home';
import MyAccount from '@/pages/MyAccount';

function Router() {
  const { isAuthenticated } = useAuth();
  return (
    <>
      {!isAuthenticated && (
        <BrowserRouter>
          <Routes>
            <Route path='/' element={<AuthLogin />} />
            <Route path='/auth/login' element={<AuthLogin />} />
            <Route path='/auth/register' element={<AuthRegister />} />
          </Routes>
        </BrowserRouter>
      )}
      {isAuthenticated && (
        <BrowserRouter>
          <Navbar />
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/my-account' element={<MyAccount />} />
          </Routes>
        </BrowserRouter>
      )}
    </>
  );
}

function App() {
  return (
    <Providers>
      <Router />
    </Providers>
  );
}

export default App;
