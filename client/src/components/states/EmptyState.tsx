type Props = {
  title: string;
  description: string;
  children: any;
};

const EmptyState = ({ title, description, children }: Props) => {
  return (
    <div className='grid gap-4 w-full'>
      <div className='w-20 h-20 mx-auto bg-blue-700 rounded-full shadow-sm justify-center items-center inline-flex'>
        {children}
      </div>
      <div>
        <h2 className='text-center text-white text-base font-semibold leading-relaxed pb-1'>
          {title}
        </h2>
        <p className='text-center text-white text-sm font-normal leading-snug pb-4'>
          {description}
        </p>
      </div>
    </div>
  );
};

export default EmptyState;
