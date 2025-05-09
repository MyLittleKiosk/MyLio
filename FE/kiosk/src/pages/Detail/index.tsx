import { DETAIL_RESPONSE } from '@/service/mock/dummies/Order';
import { formatNumber } from '@/utils/formatNumber';

const Detail = () => {
  return (
    <section className='flex flex-col gap-4 w-3/4'>
      <div className='flex items-center gap-4 pb-4 justify-between'>
        <img
          className='w-[350px]'
          src={DETAIL_RESPONSE.data.contents[0].image_url}
          alt='drink'
        />
        <div className='font-preBold text-xl flex flex-col gap-4'>
          <h1>{DETAIL_RESPONSE.data.contents[0].name}</h1>
          <span>
            {formatNumber(DETAIL_RESPONSE.data.contents[0].base_price)}원
          </span>
        </div>
      </div>
      <div>
        <span className='text-xs text-gray-500 font-preBold'>
          *1회 제공량 기준: 24oz
        </span>
        <div className='grid grid-cols-2 gap-x-9 gap-y-4 border-t-2 border-b-2 border-black py-4'>
          {Object.values(DETAIL_RESPONSE.data.contents[0].nutrition_info).map(
            (item) => (
              <div
                key={item.nutrition_name}
                className='flex items-center gap-2 justify-between font-preBold text-xs'
              >
                <span>{`${item.nutrition_name}(${item.nutrition_type})`}</span>
                <span className='font-normal'>{item.nutrition_value}</span>
              </div>
            )
          )}
        </div>
      </div>
    </section>
  );
};

export default Detail;
