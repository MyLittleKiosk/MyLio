import useOrderStore from '@/stores/useOrderStore';
import { formatNumber } from '@/utils/formatNumber';
import clsx from 'clsx';

const Order = () => {
  const { order } = useOrderStore();
  console.log('order:', order);
  const menu = order.contents[0];
  // 이미지 경로 예시 (실제 경로에 맞게 수정)
  // const imageUrl = menu.imageUrl || '/images/americano.jpg';

  return (
    order.contents[0] && (
      <section className='flex flex-col w-full h-full pt-5'>
        <h1 className='text-2xl font-preBold inline-block ps-10 mb-4'>
          메뉴 주문
        </h1>
        <div className='flex flex-col items-center w-4/5 mx-auto justify-between overflow-y-auto'>
          <div className='flex items-center justify-center mb-1 w-full gap-4'>
            <img
              src={menu.imageUrl}
              alt={menu.name}
              className='w-24 h-24 object-cover rounded-xl mx-auto'
            />
            <div className='w-full h-full p-4 flex flex-col gap-4 justify-between'>
              <div>
                <p className='text-2xl font-preBold'>{menu.name}</p>
                <p className='text-xs text-gray-500 break-keep'>
                  {menu.description}
                </p>
              </div>
              <p className='text-xl font-preBold'>
                {formatNumber(menu.totalPrice)}원
              </p>
            </div>
          </div>
          <div className='flex flex-col h-full w-full overflow-y-auto mb-36 gap-2'>
            {menu.options.map((opt) => (
              <div key={opt.optionId} className='flex gap-2 items-center'>
                <div className='flex flex-col'>
                  <div className='flex gap-2 items-center'>
                    <p className='text-lg font-preBold'>{opt.optionName}</p>
                    {opt.required && (
                      <span className='text-sm text-red-500'>필수</span>
                    )}
                  </div>
                  <div className='flex gap-2'>
                    {opt.optionDetails.map((detail) => (
                      <div
                        key={detail.optionDetailId}
                        className={clsx(
                          'text-sm text-gray-500 px-2 py-1 rounded-md break-keep',
                          opt.selectedId === detail.optionDetailId
                            ? 'bg-primary text-white'
                            : 'bg-gray-200 text-gray-500'
                        )}
                      >
                        {detail.optionDetailValue}
                        {detail.additionalPrice > 0 && (
                          <span
                            className={clsx(
                              'text-sm text-gray-500',
                              opt.selectedId === detail.optionDetailId
                                ? 'text-white'
                                : 'text-gray-500'
                            )}
                          >
                            {` (+${formatNumber(detail.additionalPrice)}원)`}
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    )
  );
};

export default Order;
