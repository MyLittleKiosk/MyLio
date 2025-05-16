import useOrderStore from '@/stores/useOrderStore';
import { useMemo, useState } from 'react';

const Menus = () => {
  const { order } = useOrderStore();
  const [page, setPage] = useState(0);
  const menus = useMemo(() => {
    if (order.contents.length === 0) return [];
    const itemsPerPage = 16;
    const totalPages = Math.ceil(order.contents.length / itemsPerPage);
    const result = [];
    console.log('order.contents:', order.contents);
    for (let i = 0; i < totalPages; i++) {
      const start = i * itemsPerPage;
      const end = start + itemsPerPage;
      result.push(order.contents.slice(start, end));
    }
    console.log('result:', result);
    return result;
  }, [order.contents]);
  return (
    <section className='flex flex-col w-full h-full pt-10'>
      <h1 className='text-2xl font-preBold inline-block ps-10'>메뉴</h1>
      <div className='w-full items-start mb-4 ps-10'>
        <span className='font-preBold text-gray-500 text-sm'>
          총 {order.contents.length}개의 메뉴
        </span>
      </div>
      <div className='flex justify-between items-center w-[95%] mx-auto h-full'>
        <div className='flex h-full items-center justify-center gap-2'>
          <button onClick={() => setPage(page - 1)} disabled={page === 0}>
            {'<'}
          </button>
        </div>
        <div className='grid grid-cols-4 h-full justify-items-center gap-y-3 gap-x-1 overflow-y-auto w-11/12 overflow-x-hidden'>
          {menus[page]?.map((item) => {
            return (
              <div
                key={item.menuId}
                className='flex flex-col items-center justify-center h-[180px] text-center whitespace-nowrap tracking-[-0.1em] rounded-3xl'
              >
                <img
                  src={item.imageUrl}
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
        <button
          onClick={() => setPage(page + 1)}
          disabled={page === menus.length - 1}
        >
          {'>'}
        </button>
      </div>
    </section>
  );
};
export default Menus;
