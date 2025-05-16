import useOrderStore from '@/stores/useOrderStore';
import { formatNumber } from '@/utils/formatNumber';

const Order = () => {
  const { order } = useOrderStore();
  console.log('order:', order);
  const menu = order.contents[0];
  // 이미지 경로 예시 (실제 경로에 맞게 수정)
  // const imageUrl = menu.imageUrl || '/images/americano.jpg';

  return (
    order.contents[0] && (
      <section className='flex flex-col w-full h-full pt-10'>
        <h1 className='text-2xl font-preBold inline-block ps-10'>메뉴 주문</h1>
        <div className='flex flex-col items-center w-4/5 mx-auto py-8 h-full justify-between'>
          {/* 이미지 슬라이드 스타일 */}
          <div className='flex items-center justify-center mb-4 w-full border-2 border-gray-300 rounded-xl gap-4'>
            {/* 좌우 흐릿한 이미지 */}
            <img
              src={menu.imageUrl}
              alt={menu.name}
              className='w-[40%] object-cover rounded-xl mx-auto'
            />
            <div className='w-full h-full p-4 flex flex-col gap-4 justify-between'>
              <p className='text-2xl font-preBold'>{menu.name}</p>
              {/* <p className='text-sm font-bold'>{menu.description}</p> */}
              <div className='flex flex-col h-full'>
                {menu.selectedOption.map((opt) => (
                  <div key={opt.optionId} className='flex gap-2 items-center'>
                    <img
                      src='/src/assets/images/check.png'
                      alt='check'
                      className='w-6 h-6'
                    />
                    <p>{opt.optionName}</p>
                    <p>
                      {opt.optionDetails
                        .map((detail) => detail.optionDetailValue)
                        .join(', ')}
                    </p>
                  </div>
                ))}
              </div>
              <p className='text-xl font-preBold text-end'>
                {formatNumber(menu.totalPrice)}원
              </p>
            </div>
          </div>
        </div>
      </section>
    )
  );
};

export default Order;
