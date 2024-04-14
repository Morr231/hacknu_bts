import { useState, useEffect } from 'react';

import { HomeIcon } from 'lucide-react';

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';

import { Button } from '@/components/ui/button';

import usePartners from '@/hooks/usePartners';
import useCreatePayment from '@/hooks/useCreatePayment';

type PartnerCardProps = {
  name: string;
  address: string;
  description: string;
  id: string;
};

const PartnerCard = ({
  name,
  address,
  description,
  id,
}: PartnerCardProps) => {
  const { data, isSuccess, isLoading, isFetching, isError, error } = usePartners(id);
  const createPaymentMutation = useCreatePayment();

  const [open, setOpen] = useState(false);
  const [partners, setPartners] = useState([]);

  useEffect(() => {
    if (isSuccess && data?.data) {
      setPartners(data.data);
    }
  }, [isSuccess, data?.data]);

  if (isLoading || isFetching) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>Error: {error?.message}</div>;
  }

  const handleClick = (
    card_type_id: number,
    cashback_percent: number,
    category_id: number,
  ) => {
    createPaymentMutation.mutate(
      {
        card_type_id: card_type_id,
        cashback_percent: cashback_percent,
        category_id: category_id,
       },
      {
        onSuccess: (data) => {
          console.log('data', data);
          setOpen(false);
        },
        onError: (error) => {
          console.log('error', error);
        },
      },
    );
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger className='max-w-screen-sm mx-auto'>
        <div className='max-w-sm rounded-xl shadow-lg border cursor-pointer bg-gray-800 text-white'>
          <div className='px-6 py-4'>
            <div className='font-bold text-xl mb-2'>
              {name}
            </div>
            <div className='flex flex-col gap-2'>
              <p className='text-gray-300 text-sm flex align-center gap-2'>
                <HomeIcon />
                <span className='text-gray-500'>City:</span> {address}
              </p>
              <p className='text-gray-300 text-sm'
                dangerouslySetInnerHTML={{ __html: description }}
              ></p>
            </div>
          </div>
        </div>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Partner offers</DialogTitle>
          <DialogDescription>
            Get partner cashback offers from {name}
          </DialogDescription>
          <div className="flex flex-col gap-2">

          {partners.sort((a, b) => a.cashback_percent > b.cashback_percent).map((partner, idx) => (
            <div className={`flex gap-2 items-center`}>
             <div className={`w-full flex justify-between items-center gap-2 border border-white p-4 rounded-xl ${idx === 0 && "border border-8 border-blue-400"}`}>
              <div className='flex justify-between items-center'>{partner.bank.name} {partner.card_type.name}</div>
              <p className='bg-green-500 p-2 rounded-xl'>Cashback: {partner.cashback_percent}%</p>
             </div>
             <Button className='px-6'
              onClick={() => handleClick(partner.card_type.id, partner.cashback_percent, partner.category.id)}
              >Pay</Button>

            </div>
          ))}
          </div>
          
        </DialogHeader>
      </DialogContent>
    </Dialog>
  );
};

export default PartnerCard;
