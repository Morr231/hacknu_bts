import { User, CircleDollarSign } from 'lucide-react';

import NavLinkItem from './nav-link-item';

const itemsArray = [
  {
    title: 'Search cashback',
    icon: CircleDollarSign,
    redirect: '/',
  },
  {
    title: 'My account',
    icon: User,
    redirect: '/my-account',
  },
];

const NavLinks = () => {
  return (
    <ul className='flex items-center justify-between gap-4'>
      {itemsArray.map((item, index) => {
        return <NavLinkItem key={index} {...item} />;
      })}
    </ul>
  );
};

export default NavLinks;
