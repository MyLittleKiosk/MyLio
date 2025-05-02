import { DETAIL_RESPONSE } from '@/service/mock/dummies/Order';
import { formatNumber } from '@/utils/formatNumber';

const Detail = () => {
  return (
    <section className='flex flex-col gap-4 w-3/4'>
      <div className='flex items-center gap-4 pb-4 justify-between'>
        <img
          className='w-[350px]'
          src={DETAIL_RESPONSE.detail.image}
          alt='drink'
        />
        <div className='font-bold text-xl flex flex-col gap-4'>
          <h1>{DETAIL_RESPONSE.detail.name}</h1>
          <span>{formatNumber(DETAIL_RESPONSE.detail.price)}원</span>
        </div>
      </div>
      <div>
        <span className='text-xs text-gray-500 font-bold'>
          *1회 제공량 기준: 24oz
        </span>
        <div className='grid grid-cols-2 gap-x-9 gap-y-4 border-t-2 border-b-2 border-black py-4'>
          {Object.values(DETAIL_RESPONSE.detail.nutrition).map((item) => (
            <div
              key={item.name}
              className='flex items-center gap-2 justify-between font-bold text-xs'
            >
              <span>{`${item.name}(${item.unit})`}</span>
              <span className='font-normal'>{item.value}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Detail;
