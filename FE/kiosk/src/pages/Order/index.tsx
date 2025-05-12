import useOrderStore from '@/stores/useOrderStore';

const Order = () => {
  const { order } = useOrderStore();

  const menu = order.contents[0];
  const cartItem = order.cart?.[0];

  // 이미지 경로 예시 (실제 경로에 맞게 수정)
  // const imageUrl = menu.imageUrl || '/images/americano.jpg';

  return (
    <div className='flex flex-col items-center w-full py-8 h-full justify-between'>
      {/* 상단 슬라이드 점 */}
      <div className='flex justify-center items-center mb-2 gap-1'>
        <div className='w-2 h-2 rounded-full bg-gray-300' />
        <div className='w-2 h-2 rounded-full bg-blue-400' />
        <div className='w-2 h-2 rounded-full bg-gray-300' />
      </div>
      {/* 이미지 슬라이드 스타일 */}
      <div className='relative flex items-center justify-center mb-4 w-full'>
        {/* 좌우 흐릿한 이미지 */}
        <img
          src={menu.imageUrl}
          // src={'/src/assets/images/defaultDrink.png'}
          alt={menu.name}
          className='w-32 h-32 object-cover rounded-xl z-10 mx-auto'
        />
      </div>
      {/* 메뉴명 */}
      <h2 className='text-lg font-bold mb-2'>{menu.name}</h2>
      {/* 선택된 옵션(라지) */}
      <div className='mb-2 flex flex-col gap-2 items-center px-4'>
        {menu.options.map((opt) => (
          <div className='flex gap-2' key={opt.optionId}>
            {opt.optionDetails.map((detail) => (
              <span
                key={detail.optionDetailId}
                className={`px-4 py-1 ${detail.optionDetailId === opt.selectedId ? 'bg-blue-500 text-white' : 'bg-gray-200'} rounded-lg text-sm font-semibold`}
              >
                {detail.optionDetailValue}
                {detail.additionalPrice > 0 &&
                  ` (+${detail.additionalPrice}원)`}
                {detail.additionalPrice < 0 && ` (${detail.additionalPrice}원)`}
              </span>
            ))}
          </div>
        ))}
      </div>
      {/* 가격 */}
      <div className='text-xl font-bold mb-2'>
        ₩{' '}
        {cartItem?.totalPrice?.toLocaleString() ??
          menu.basePrice?.toLocaleString()}
      </div>
    </div>
  );
};

export default Order;
