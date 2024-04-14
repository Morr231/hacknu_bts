import { Link } from 'react-router-dom';

import NavLinks from './nav-links';
import H4 from '@/components/typo/H4';

const navbar = () => {
  return (
    <header className='fixed top-0 overflow-hidden w-full flex items-center justify-between px-4 h-16 z-10 border-b bg-black'>
      <div className='max-w-screen-lg m-auto w-full flex items-center'>
        <Link to='/'>
          <H4 className='mr-8'>unemdeu.</H4>
        </Link>
        <div className='flex items-center justify-center gap-4'>
          <NavLinks />
        </div>
      </div>
    </header>
  );
};

export default navbar;
