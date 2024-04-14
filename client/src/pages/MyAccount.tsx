import { CreditCard } from 'lucide-react';

import AddCardDialog from './AddCardDialog';
import Card from './Card';
import UserCard from './UserCard';
import { useAuth } from '@/components/contexts/AuthContext';
import EmptyState from '@/components/states/EmptyState';
import Wrapper from '@/components/wrapper';
import ViewHistoryDialog from './ViewHistoryDialog';

const MyAccount = () => {
  const { profile } = useAuth();

  return (
    <Wrapper className='flex flex-col items-center gap-4'>
      <UserCard profile={profile} />
      <ViewHistoryDialog profile={profile}/>
      <AddCardDialog />

      {profile.bank_cards.map((card: any) => (
        <Card
          key={card.id}
          bank={card.bank.name}
          cardType={card.card_type.name}
          cardNumber={card.card_number}
        />
      ))}

      {profile.bank_cards.length === 0 && (
        <EmptyState
          title='No cards added'
          description='You have not added any cards to your account.'
        >
          <CreditCard size={48} />
        </EmptyState>
      )}
    </Wrapper>
  );
};

export default MyAccount;
