type UserCardProps = {
  profile: any;
};

const UserCard = ({ profile }: UserCardProps) => {
  return (
    <div className='shadow rounded-lg border max-w-screen-sm w-full bg-gray-800'>
      <div className='px-4 py-5 sm:px-6'>
        <h3 className='text-lg leading-6 font-medium'>User Profile</h3>
        <p className='mt-1 max-w-2xl text-sm'>
          This is some information about the user.
        </p>
      </div>
      <div className='border-t border-gray-200 px-4 py-5 sm:p-0'>
        <dl className='sm:divide-y sm:divide-gray-200'>
          <div className='py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6'>
            <dt className='text-sm font-medium'>Full name</dt>
            <dd className='mt-1 text-sm sm:mt-0 sm:col-span-2'>
              {profile.full_name}
            </dd>
          </div>
          <div className='py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6'>
            <dt className='text-sm font-medium'>Email address</dt>
            <dd className='mt-1 text-sm sm:mt-0 sm:col-span-2'>
              {profile.email}
            </dd>
          </div>
          <div className='py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6'>
            <dt className='text-sm font-medium'>Phone number</dt>
            <dd className='mt-1 text-sm sm:mt-0 sm:col-span-2'>
              {profile.phone_number}
            </dd>
          </div>
          <div className='py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6'>
            <dt className='text-sm font-medium'>City</dt>
            <dd className='mt-1 text-sm sm:mt-0 sm:col-span-2'>
              {profile.city.name}
            </dd>
          </div>
        </dl>
      </div>
    </div>
  );
};

export default UserCard;
