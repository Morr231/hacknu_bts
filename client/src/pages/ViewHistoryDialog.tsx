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



const ViewHistoryDialog = (
  profile: any
) => {
  const [open, setOpen] = useState(false);

  console.log('profile', profile);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger className='w-full max-w-screen-sm'>
        <Button className='w-full max-w-screen-sm mt-2'>View history</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Your history</DialogTitle>
          <DialogDescription>
              View your history here
            </DialogDescription>

         {
            profile.profile?.payments?.map((item: any) => {
              return (
                <div className='flex justify-between border border-white rounded-xl p-4'>
                  <div>{item.bank_name} {item.card_type.name}</div>
                  <div>Cashback: {item.cashback_percent}%</div>
                  <div>Category: {item.category.name}</div>
                </div>
              )
            })
         }
           
        </DialogHeader>
      </DialogContent>
    </Dialog>
  );
};

export default ViewHistoryDialog;
