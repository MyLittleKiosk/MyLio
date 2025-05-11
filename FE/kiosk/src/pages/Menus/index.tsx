import useOrderStore from '@/stores/useOrderStore';
const Menus = () => {
  const { order } = useOrderStore();
  return (
    <section className='flex flex-col w-full h-full ps-10 pt-10'>
      <h1 className='text-2xl font-preBold inline-block'>메뉴</h1>
      <div className='w-full items-start mb-4'>
        <span className='font-preBold text-gray-500 text-sm'>
          총 {order.contents.length}개의 메뉴
        </span>
      </div>
      <div className='grid grid-cols-4 justify-items-center gap-5 overflow-y-auto'>
        {order.contents.map((item) => {
          return (
            <div
              key={item.menuId}
              className='flex flex-col items-center justify-center w-[1/4] h-[180px] text-center whitespace-nowrap tracking-[-0.1em] rounded-3xl'
            >
              <img
                // src={item.imageUrl}
                src={'/src/assets/images/defaultDrink.png'}
                alt={item.name}
                className='w-full h-[90px] max-w-[90px] mx-auto'
              />
              <div className='flex flex-col items-center h-[100px] justify-center mx-auto'>
                <h1 className='text-sm font-preBold'>{item.name}</h1>
                <h1 className='text-sm font-preBold'>
                  {item.basePrice.toLocaleString()}원
                </h1>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default Menus;
