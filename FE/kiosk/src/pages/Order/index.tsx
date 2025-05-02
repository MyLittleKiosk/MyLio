import { MenuResponse } from '@/service/mock/dummies/Order';

const Order = () => {
  return (
    <section className='flex flex-col w-full h-full justify-center items-center p-10'>
      <h1 className='text-2xl font-bold mb-10'>주문하기</h1>
      <div className='w-full items-start mb-2'>
        <span className='font-bold'>
          총 {MenuResponse.menu.length}개의 메뉴
        </span>
      </div>
      <div className='grid grid-cols-4 justify-items-start gap-5 overflow-y-auto h-[75%] w-full'>
        {MenuResponse.menu.map((item) => {
          return (
            <div
              key={item.id}
              className='flex flex-col items-center justify-center w-[180px] h-[180px] text-center break-keep border-2 border-gray-300 rounded-3xl'
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

export default Order;
