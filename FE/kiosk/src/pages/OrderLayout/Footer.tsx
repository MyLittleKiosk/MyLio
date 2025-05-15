import RecordButton from '@/components/Chat/RecordButton';
import clsx from 'clsx';
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
  return (
    <div
      className={clsx(
        'flex px-4 pt-4 items-center fixed bottom-4 left-0 w-full h-[250px] bg-white',
        FOOTER_PATHS.includes(pathname) ? 'justify-between' : 'justify-end'
      )}
    >
      {FOOTER_PATHS.includes(pathname) && (
        <div className='px-4 flex justify-start items-center gap-4 bg-gray-200 w-[80%] h-full rounded-xl overflow-y-auto'>
          {order.cart.map((item) => (
            <div
              key={item.cartId}
              className='w-1/4 h-[80%] flex flex-col bg-white rounded-xl justify-center items-center gap-2'
            >
              <img src={item.imageUrl} alt={item.name} />
              <p className='text-sm'>{item.quantity}</p>
            </div>
          ))}
        </div>
      )}
      <RecordButton onRecognitionResult={handleRecognitionResult} />
    </div>
  );
};

export default Footer;
