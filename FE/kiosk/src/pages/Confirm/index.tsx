import { formatNumber } from '@/utils/formatNumber';
import useOrderStore from '@/stores/useOrderStore';
const Confirm = () => {
  const { order } = useOrderStore();
  return (
    <section className='flex flex-col w-full h-full ps-10 pt-10'>
      <h1 className='text-2xl font-preBold'>주문확인</h1>
      <div className='flex flex-col gap-2 mt-10 w-full overflow-y-auto'>
        {order.contents.map((item) => (
          <div key={item.menuId} className='flex items-center gap-2'>
            <img src={item.imageUrl} alt={item.name} />
            <div className='flex flex-col w-1/2'>
              <h2 className='text-lg font-preBold'>{item.name}</h2>
              <p>{formatNumber(item.basePrice)}</p>
              {item.options.map((option) => (
                <p key={option.optionName} className='text-xs text-gray-500'>
                  <div className='flex items-center justify-between'>
                    <div>{option.optionName}</div>{' '}
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
