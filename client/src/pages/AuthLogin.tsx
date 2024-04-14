import { useAuth } from '@/components/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import Wrapper from '@/components/wrapper';

const AuthLogin = () => {
  const { handleLogin } = useAuth();

  const handleClickLogin = (e: any) => {
    e.preventDefault();

    handleLogin({
      username: e.target.email.value,
      password: e.target.password.value,
    });
  };

  return (
    <Wrapper className='flex flex-col items-center justify-center'>
      <div className='max-w-screen-sm flex flex-col gap-4'>
        <h1 className='text-3xl font-bold text-center'>Login</h1>
        <form
          className='max-w-screen-sm flex flex-col gap-4'
          onSubmit={handleClickLogin}
        >
          <Input type='email' placeholder='Email' name='email' />
          <Input type='password' placeholder='Password' name='password' />
          <Button>Login</Button>
        </form>
        <div className='text-center'>
          no account?{' '}
          <a href='/auth/register' className='text-blue-300'>
            Register
          </a>
        </div>
      </div>
    </Wrapper>
  );
};

export default AuthLogin;
