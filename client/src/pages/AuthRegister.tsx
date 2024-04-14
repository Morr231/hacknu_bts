import { useEffect, useState } from 'react';

import { useAuth } from '@/components/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import Wrapper from '@/components/wrapper';
import useCities from '@/hooks/useCities';

const AuthRegister = () => {
  const { handleRegister } = useAuth();

  const [cities, setCities] = useState<any[]>([]);
  const [selectedCity, setSelectedCity] = useState<string>('');
  const { data, isSuccess, isLoading, isFetching, isError, error } =
    useCities();

  useEffect(() => {
    if (isSuccess && data?.data) {
      setCities(data.data.cities);
    }
  }, [isSuccess, data?.data]);

  if (isLoading || isFetching) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>Error: {error?.message}</div>;
  }

  const handleClickRegister = (e: any) => {
    e.preventDefault();

    handleRegister({
      email: e.target.email.value,
      password: e.target.password.value,
      full_name: `${e.target.name.value} ${e.target.surname.value}`,
      phone_number: e.target.phone.value,
      city_id: selectedCity,
    });
  };

  return (
    <Wrapper className='flex flex-col items-center justify-center'>
      <div className='max-w-screen-sm flex flex-col gap-4'>
        <h1 className='text-3xl font-bold text-center'>Register</h1>
        <form
          className='max-w-screen-sm flex flex-col gap-4'
          onSubmit={handleClickRegister}
        >
          <Input type='email' placeholder='Email' name='email' />
          <Input type='password' placeholder='Password' name='password' />
          <div className='flex gap-2'>
            <Input type='text' placeholder='Name' name='name' />
            <Input type='text' placeholder='Surname' name='surname' />
          </div>
          <Input type='text' placeholder='Phone' name='phone' />
          <Select
            onValueChange={setSelectedCity}
            defaultValue={selectedCity}
            required
          >
            <SelectTrigger>
              <SelectValue placeholder='City' />
            </SelectTrigger>
            <SelectContent>
              {cities.map((city) => (
                <SelectItem key={city.id} value={city.id.toString()}>
                  {city.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button type='submit'>Register</Button>
        </form>
        <div className='text-center'>
          have account?{' '}
          <a href='/auth/login' className='text-blue-300'>
            login
          </a>
        </div>
      </div>
    </Wrapper>
  );
};

export default AuthRegister;
