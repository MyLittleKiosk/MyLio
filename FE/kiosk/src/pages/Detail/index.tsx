import useOrderStore from '@/stores/useOrderStore';
import { formatNumber } from '@/utils/formatNumber';
const Detail = () => {
  const { order } = useOrderStore();
  return (
    <section className='flex flex-col gap-4 w-3/4'>
      <h1 className='text-2xl font-bold'>성분 정보</h1>
      {order.contents[0] && (
        <>
          <div className='flex items-center gap-4 pb-4 justify-between'>
            <img
              className='w-[200px] rounded-xl'
              src={order.contents[0].imageUrl}
              alt='drink'
            />
            <div className='font-preBold text-xl flex flex-col gap-4'>
              <h1 className='text-2xl font-bold'>{order.contents[0].name}</h1>
              <span className='text-xl font-bold'>
                {formatNumber(order.contents[0].basePrice)}원
              </span>
            </div>
          </div>
          <div>
            <span className='text-xs text-gray-500 font-preBold'>
              *1회 제공량 기준: 24oz
            </span>
            <div className='grid grid-cols-2 gap-x-9 gap-y-4 border-t-2 border-b-2 border-black py-4'>
              {Object.values(order.contents[0].nutritionInfo).map((item) => (
                <div
                  key={item.nutritionName}
                  className='flex items-center gap-2 justify-between font-preBold text-xs'
                >
                  <span>{`${item.nutritionName}(${item.nutritionType})`}</span>
                  <span className='font-normal'>{item.nutritionValue}</span>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </section>
  );
};

export default Detail;
