import RecordButton from '@/components/Chat/RecordButton';
import clsx from 'clsx';
import { useMemo, useState } from 'react';
const FOOTER_PATHS = [
  '/kiosk/search',
  '/kiosk',
  '/kiosk/order',
  '/kiosk/detail',
];

interface FooterProps {
  order: {
    cart: {
      cartId: string;
      imageUrl: string;
      name: string;
      quantity: number;
    }[];
  };
  handleRecognitionResult: (text: string) => void;
  pathname: string;
}

const Footer = ({ order, handleRecognitionResult, pathname }: FooterProps) => {
  const [page, setPage] = useState(0);
  const cartList = useMemo(() => {
    if (order.cart.length === 0) return [];
    const itemsPerPage = 4;
    const totalPages = Math.ceil(order.cart.length / itemsPerPage);
    const result = [];
    for (let i = 0; i < totalPages; i++) {
      const start = i * itemsPerPage;
      const end = start + itemsPerPage;
      result.push(order.cart.slice(start, end));
    }
    return result;
  }, [order.cart]);
  return (
    <div
      className={clsx(
        'flex px-4 pt-4 items-center fixed bottom-4 left-0 w-full h-[250px] bg-white',
        FOOTER_PATHS.includes(pathname) ? 'justify-between' : 'justify-end'
      )}
    >
      {FOOTER_PATHS.includes(pathname) && (
        <div className='px-2 flex justify-between items-center gap-4 bg-gray-200 w-[80%] h-full rounded-xl overflow-y-auto'>
          <div className='flex items-center gap-2 '>
            <button onClick={() => setPage(page - 1)} disabled={page === 0}>
              {'<'}
            </button>
          </div>
          <div className='flex items-center gap-2 w-full'>
            {cartList[page]?.map((item) => (
              <div
                key={item.cartId}
                className='w-1/4 h-[80%] flex flex-col bg-white rounded-xl justify-center items-center gap-2'
              >
                <img
                  src={item.imageUrl}
                  alt={item.name}
                  className='w-24 h-24 object-cover'
                />
                <p className='text-sm'>{item.quantity}</p>
              </div>
            ))}
          </div>
          <button
            onClick={() => setPage(page + 1)}
            disabled={page === cartList.length - 1}
          >
            {'>'}
          </button>
        </div>
      )}
      <RecordButton onRecognitionResult={handleRecognitionResult} />
    </div>
  );
};

export default Footer;
