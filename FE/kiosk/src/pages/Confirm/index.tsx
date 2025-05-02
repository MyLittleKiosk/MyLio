import { CONFIRM_RESPONSE } from '@/service/mock/dummies/Order';
import { formatNumber } from '@/utils/formatNumber';
import { useMemo } from 'react';
const Confirm = () => {
  return (
    <section className='flex flex-col w-full h-full ps-10 pt-10'>
      <h1 className='text-2xl font-bold'>주문확인</h1>
      <div className='flex flex-col gap-2 mt-10 w-full overflow-y-auto'>
        {CONFIRM_RESPONSE.confirm.map((item) => (
          <div key={item.id} className='flex items-center gap-2'>
            <img src={item.image} alt={item.name} />
            <div className='flex flex-col w-1/2'>
              <h2 className='text-lg font-bold'>{item.name}</h2>
              <p>{formatNumber(item.price)}</p>
              {item.options.map((option) => (
                <p key={option.name} className='text-xs text-gray-500'>
                  <div className='flex items-center justify-between'>
                    <div>{option.name}</div>{' '}
                    <div>+{formatNumber(option.price)}</div>
                  </div>
                </p>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Confirm;
