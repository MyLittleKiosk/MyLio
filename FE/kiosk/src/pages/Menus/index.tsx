import useOrderStore from '@/stores/useOrderStore';
import clsx from 'clsx';
import { useEffect, useMemo, useState } from 'react';

const Menus = () => {
  const { order } = useOrderStore();
  const [page, setPage] = useState(0);

  const menus = useMemo(() => {
    if (order.contents.length === 0) {
      setPage(0);
      return [];
    }

    const itemsPerPage = 9;
    const totalPages = Math.ceil(order.contents.length / itemsPerPage);
    const result = [];

    for (let i = 0; i < totalPages; i++) {
      const start = i * itemsPerPage;
      const end = start + itemsPerPage;
      result.push(order.contents.slice(start, end));
    }

    if (totalPages === 1) {
      setPage(0);
    }

    return result;
  }, [order.contents]);

  useEffect(() => {
    setPage(0);
  }, [order.contents]);

  return (
    <section className='flex flex-col w-full h-full pt-5'>
      <h1 className='text-2xl font-preBold inline-block ps-10'>메뉴</h1>
      <div className='w-full items-start mb-4 ps-10'>
        <span className='font-preBold text-gray-500 text-sm'>
          총 {order.contents.length}개의 메뉴
        </span>
      </div>
      <div className='flex justify-between w-[95%] mx-auto h-[65%]'>
        <div className='flex h-full items-center justify-center gap-2'>
          <button
            onClick={() => setPage(page - 1)}
            disabled={page === 0}
            className={clsx('block', page === 0 && 'opacity-0 invisible')}
          >
            {'<'}
          </button>
        </div>
        <div className='grid grid-cols-3 justify-items-center items-start gap-1 overflow-y-auto w-11/12 overflow-x-hidden'>
          {menus[page]?.map((item) => {
            return (
              <div
                key={item.menuId}
                className='flex flex-col items-start justify-center text-center whitespace-nowrap tracking-[-0.1em] rounded-3xl'
              >
                <img
                  src={item.imageUrl}
                  alt={item.name}
                  className='w-[130px] h-[130px] object-cover mx-auto rounded-lg'
                />
                <div className='flex flex-col items-center h-[100px] justify-center mx-auto'>
                  <h1 className='text-sm font-preBold'>{item.name}</h1>
                  <h1 className='text-xs font-preBold text-gray-400'>
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
          className={clsx(
            'block',
            page === menus.length - 1 && 'opacity-0 invisible'
          )}
        >
          {'>'}
        </button>
      </div>
      <div className='flex justify-center items-center gap-2 mt-1'>
        {menus.map((_, index) => (
          <div
            key={index}
            className={`w-2 h-2 rounded-full transition-all duration-200 ${
              page === index ? 'bg-black scale-125' : 'bg-subContent'
            }`}
          />
        ))}
      </div>
    </section>
  );
};
export default Menus;
