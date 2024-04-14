import { useState, useEffect } from 'react';

import { CircleDollarSign, Search } from 'lucide-react';

import PartnerCard from './PartnerCard';
import EmptyState from '@/components/states/EmptyState';
import H2 from '@/components/typo/H2';
import H3 from '@/components/typo/H3';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import Wrapper from '@/components/wrapper';
import useCategories from '@/hooks/useCategories';
import useSearch from '@/hooks/useSearch';
import useCategoryPartners from '@/hooks/useCategoryPartners';
import useCreatePayment from '@/hooks/useCreatePayment';

const Home = () => {
  const [currentFilter, setCurrentFilter] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const { data, isSuccess, isLoading, isFetching, isError, error } =  useCategories();
  const { data: categoryPartnersData, isSuccess: categoryPartnersIsSuccess } = useCategoryPartners(currentFilter);
  const createPaymentMutation = useCreatePayment();

  const [searchData, setSearchData] = useState([]);
  const [categoryPartners, setCategoryPartners] = useState([]);

  const searchMutation = useSearch();
  const [categories, setCategories] = useState<any[]>([]);

  useEffect(() => {
    if (isSuccess && data?.data) {
      setCategories(data.data);
    }
  }, [isSuccess, data?.data]);

  console.log('categoryPartnersData', categoryPartnersData);

  useEffect(() => {
    if (categoryPartnersIsSuccess && categoryPartnersData?.data) {
      setCategoryPartners(categoryPartnersData.data);
    }
  } , [categoryPartnersIsSuccess, categoryPartnersData?.data]);

  const handleSearch = () => {
    searchMutation.mutate(
      { name: searchQuery },
      {
        onSuccess: (data) => {
          console.log('data', data);
          setSearchData(data.data);
        },
        onError: (error) => {
          setSearchData([]);
        },
      },
    );
  };

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
        },
        onError: (error) => {
          console.log('error', error);
        },
      },
    );
  }

  return (
    <Wrapper className='flex flex-col items-center max-w-screen-md mx-auto gap-4'>
      <div className='w-full'>
        <H2 className='mt-4'>Search cashback</H2>
        <div className='flex gap-4'>
          <Input
            className='mt-4'
            placeholder='Search'
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <Button className='mt-4 w-20' onClick={handleSearch}>
            <Search />
          </Button>
        </div>
      </div>
      {(!searchData || searchData?.length === 0) && (
        <EmptyState
          title='No search results found'
          description='There are no cashback offers matching your search.'
        >
          <CircleDollarSign size={48} />
        </EmptyState>
      )}

      {
        searchData?.map((partner) => (
          <PartnerCard
            key={partner.id}
            id={partner.id}
            name={partner.name}
            address={partner.address}
            description={partner.description}
          />
        ))
      }
      {(!searchData || searchData?.length === 0) &&
      <>
      
      <H3 className='mb-2'>Instead you can choose one of the filters</H3>
      <div className='flex flex-wrap gap-2'>
        {categories.map((filter) => (
          <Badge
            key={filter.id + filter.name}
            className='mr-2 text-md'
            onClick={() => setCurrentFilter(filter.id)}
            variant={currentFilter === filter.id ? 'default' : 'secondary'}
          >
            {filter.name}
          </Badge>
        ))}
      </div>
     
      

      {categoryPartners.sort((a, b) => a.cashback_percent > b.cashback_percent).map((partner, idx) => (
          <div className='flex gap-2 items-center w-full'>
          <div className={`w-full flex justify-between items-center gap-2 border border-white p-4 rounded-xl  ${idx === 0 && "border border-8 border-blue-400"}`}>
           <div className='flex justify-between items-center'>{partner.bank.name} {partner.card_type.name}</div>
           <p className='bg-green-500 p-2 rounded-xl'>Cashback: {partner.cashback_percent}%</p>
          </div>
          <Button className='px-6'
            onClick={() => handleClick(partner.card_type.id, partner.cashback_percent, partner.category.id)}
          >Pay</Button>

         </div>
      ))}
      </>
    }
    </Wrapper>
  );
};

export default Home;
