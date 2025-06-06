import { formatNumber } from '@/utils/formatNumber';
import useOrderStore from '@/stores/useOrderStore';
import Item from '@/pages/Confirm/Item';

const Confirm = () => {
  const { order } = useOrderStore();

  return (
    <section className='flex flex-col w-full h-full pt-5'>
      <h1 className='text-2xl font-preBold inline-block ps-10 mb-4'>
        주문 확인
      </h1>
      <div className='flex flex-col gap-2 ps-10 pe-10 overflow-y-auto'>
        {order.contents.map((item, idx) => (
          <Item
            key={item.menuId}
            menuId={item.menuId}
            imageUrl={item.imageUrl}
            name={item.name}
            selectedOption={item.selectedOption}
            totalPrice={item.totalPrice}
            count={item.quantity}
            isLast={idx === order.cart.length - 1}
          />
        ))}
        <div className='flex flex-col gap-2 w-full pb-6'>
          <div className='flex items-center justify-between pt-4 border-gray-200 me-4'>
            <div>총 주문금액</div>
            <div>
              {formatNumber(
                order.contents.reduce(
                  (acc, curr) => acc + curr.totalPrice * curr.quantity,
                  0
                )
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
