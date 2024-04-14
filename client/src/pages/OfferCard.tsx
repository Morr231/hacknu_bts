type OfferCardProps = {
  card: string;
  offer: string;
  specialOffer?: string;
};

const OfferCard = ({ card, offer, specialOffer }: OfferCardProps) => {
  return (
    <div className='bg-black border border-white rounded-xl w-full p-4 '>
      <div className='flex items-center justify-between'>
        <div className='flex items-center gap-2'>
          <h2 className='text-white font-bold text-xl'>{card}&apos;s</h2>
          <p className='text-white text-sm'>Cashback</p>
        </div>
        <div className='flex flex-col items-center gap-2'>
          <div className='text-white bg-green-500 px-4 py-2 rounded-lg w-40 text-center text-xl'>
            {offer}
          </div>
          {specialOffer && (
            <div className='text-white bg-blue-500 px-4 py-2 rounded-lg w-40 text-center text-xl'>
              {specialOffer}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default OfferCard;
