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
            <img
              src={item.imageUrl}
              alt={item.name}
              className='w-20 h-20 object-cover rounded-lg'
            />
            <div className='flex flex-col w-1/2'>
              <h2 className='text-lg font-preBold'>{item.name}</h2>
              <p>{formatNumber(item.totalPrice)}</p>
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
        <div className='flex flex-col gap-2 w-full pe-4'>
          <div className='flex items-center justify-between border-t pt-4'>
            <div>총 주문금액</div>
            <div>
              {formatNumber(
                order.contents.reduce((acc, curr) => acc + curr.totalPrice, 0)
              )}
              원
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Confirm;
