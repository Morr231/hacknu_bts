// @ts-ignore
import { useState, useEffect } from 'react';

import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import useBanks from '@/hooks/user/useBanks';
import useCreateCard from '@/hooks/user/useCreateCard';

const AddCardDialog = () => {
  const [open, setOpen] = useState(false);

  const createCardMutation = useCreateCard();
  const { data, isSuccess, isLoading, isFetching, isError, error } = useBanks();

  const [banks, setBanks] = useState<any[]>([]);
  const [selectedBank, setSelectedBank] = useState<string>('');
  const [selectedCardType, setSelectedCardType] = useState<string>('');

  useEffect(() => {
    if (isSuccess && data?.data) {
      setBanks(data.data.banks);
    }
  }, [isSuccess, data?.data]);

  if (isLoading || isFetching) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>Error: {error?.message}</div>;
  }

  const handleAddCard = (e: any) => {
    e.preventDefault();
    const obj = {
      card_number: e.target.card_number.value,
      bank_id: selectedBank,
      card_type_id: selectedCardType,
    };

    createCardMutation.mutate(obj, {
      onSuccess: () => {
        setOpen(false);
      },
      onError: () => {
        console.log('error');
      },
    });
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger className='w-full max-w-screen-sm'>
        <Button className='w-full max-w-screen-sm mt-2'>Add card</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Add card</DialogTitle>
          <DialogDescription>
            Enter your card details to add a new card to your account.
          </DialogDescription>

          <form className='flex flex-col gap-4' onSubmit={handleAddCard}>
            <Input
              type='text'
              placeholder='Card number'
              name='card_number'
              required
            />
            <Select
              onValueChange={setSelectedBank}
              defaultValue={selectedBank}
              required
            >
              <SelectTrigger>
                <SelectValue placeholder='Bank' />
              </SelectTrigger>
              <SelectContent>
                {banks.map((bank) => (
                  <SelectItem key={bank.id} value={bank.id.toString()}>
                    {bank.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select
              onValueChange={setSelectedCardType}
              defaultValue={selectedCardType}
              disabled={!selectedBank}
              required
            >
              <SelectTrigger>
                <SelectValue placeholder='Card type' />
              </SelectTrigger>
              <SelectContent>
                {selectedBank &&
                  banks
                    .find((bank) => bank.id.toString() === selectedBank)
                    ?.card_types.map((cardType: any) => (
                      <SelectItem
                        key={cardType.id}
                        value={cardType.id.toString()}
                      >
                        {cardType.name}
                      </SelectItem>
                    ))}
              </SelectContent>
            </Select>

            <Button type='submit'>Add card</Button>
          </form>
        </DialogHeader>
      </DialogContent>
    </Dialog>
  );
};

export default AddCardDialog;
