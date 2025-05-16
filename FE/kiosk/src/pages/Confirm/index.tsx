import { formatNumber } from '@/utils/formatNumber';
import useOrderStore from '@/stores/useOrderStore';
const Confirm = () => {
  const { order } = useOrderStore();
  return (
    <section className='flex flex-col w-full h-full pt-5'>
      <h1 className='text-2xl font-preBold inline-block ps-10 mb-4'>
        주문 확인
      </h1>
      <div className='flex flex-col gap-2 ps-10 pe-10 overflow-y-auto'>
        {order.contents.map((item) => (
          <div
            key={item.menuId}
            className='flex items-center gap-7 border-b-2 pb-4'
          >
            <img
              src={item.imageUrl}
              alt={item.name}
              className='w-20 h-20 object-cover rounded-lg'
            />
            <div className='flex flex-col w-1/2 justify-between'>
              <h2 className='text-lg font-preBold'>{item.name}</h2>
              {item.selectedOption.map((option) => (
                <p key={option.optionName} className='text-xs text-gray-500'>
                  <div className='flex items-center justify-between'>
                    <div>
                      {option.optionDetails.map((detail) => (
                        <>
                          {detail.optionDetailValue}
                          {detail.additionalPrice > 0 &&
                            ` (+${formatNumber(detail.additionalPrice)}원)`}
                        </>
                      ))}
                    </div>
                  </div>
                </p>
              ))}
              <p className='font-bold'>{formatNumber(item.totalPrice)}원</p>
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
