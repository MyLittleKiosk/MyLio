import { MenuResponse } from '@/service/mock/dummies/Order';

const Menus = () => {
  return (
    <section className='flex flex-col w-full h-full ps-10 pt-10'>
      <h1 className='text-2xl font-bold inline-block'>메뉴</h1>
      <div className='w-full items-start mb-4'>
        <span className='font-bold text-gray-500 text-sm'>
          총 {MenuResponse.menu.length}개의 메뉴
        </span>
      </div>
      <div className='grid grid-cols-4 justify-items-start gap-5 overflow-y-auto'>
        {MenuResponse.menu.map((item) => {
          return (
            <div
              key={item.id}
              className='flex flex-col items-center justify-center w-[180px] h-[180px] text-center break-keep rounded-3xl'
            >
              <img
                src={item.image}
                alt={item.name}
                className='w-[90px] h-[90px]'
              />
              <div className='flex flex-col items-center h-[100px] justify-center'>
                <h1 className='text-sm font-bold'>{item.name}</h1>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default Menus;
