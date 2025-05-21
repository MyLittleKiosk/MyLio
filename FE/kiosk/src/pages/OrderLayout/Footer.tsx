import RecordButton, { RecordButtonRef } from '@/components/Chat/RecordButton';
import clsx from 'clsx';
import { useMemo, useState, useRef, useEffect } from 'react';
import Item from '@/pages/OrderLayout/Item';
import useOrderStore from '@/stores/useOrderStore';
import { useOrderRequest } from '@/service/queries/order';
import PitchDetector, {
  PitchDetectorRef,
} from '@/components/Chat/PitchDetector';
const FOOTER_PATHS = [
  '/kiosk/search',
  '/kiosk',
  '/kiosk/order',
  '/kiosk/detail',
];

interface FooterProps {
  handleRecognitionResult: (text: string) => void;
  pathname: string;
}

const Footer = ({ handleRecognitionResult, pathname }: FooterProps) => {
  const [page, setPage] = useState(0);
  const [recordingMethod, setRecordingMethod] = useState<'pitch' | 'hold'>(
    'pitch'
  );
  const order = useOrderStore((state) => state.order);
  const { mutate } = useOrderRequest();
  const recordButtonRef = useRef<RecordButtonRef>(null);
  const pitchDetectorRef = useRef<PitchDetectorRef>(null);

  // order가 변경될 때마다 PitchDetector 초기화
  useEffect(() => {
    if (pitchDetectorRef.current) {
      pitchDetectorRef.current.reset();
    }
  }, [order]);

  const cartList = useMemo(() => {
    if (order.cart.length === 0) {
      setPage(0);
      return [];
    }

    const itemsPerPage = 4;
    const totalPages = Math.ceil(order.cart.length / itemsPerPage);
    const result = [];
    for (let i = 0; i < totalPages; i++) {
      const start = i * itemsPerPage;
      const end = start + itemsPerPage;
      result.push(order.cart.slice(start, end));
    }

    if (totalPages === 1) {
      setPage(0);
    }

    return result;
  }, [order.cart]);

  // 수량 증가
  const handleIncrease = (cartId: string) => {
    const cartItem = order.cart.find((item) => item.cartId === cartId);
    if (!cartItem) return;
    const quantity = cartItem.quantity + 1;
    mutate({
      text: `${cartItem.name}(${cartId})를 ${quantity}개로 바꿔주세요`,
      ...order,
    });
  };
  // 수량 감소
  const handleDecrease = (cartId: string) => {
    const cartItem = order.cart.find((item) => item.cartId === cartId);
    if (!cartItem) return;
    const quantity = cartItem.quantity - 1;
    mutate({
      text: `${cartItem.name}(${cartId})를 ${quantity}개로 바꿔주세요`,
      ...order,
    });
  };
  // 삭제
  const handleRemove = (cartId: string) => {
    const cartItem = order.cart.find((item) => item.cartId === cartId);
    if (!cartItem) return;
    mutate({
      text: `${cartItem.name}(${cartId})를 삭제해주세요`,
      ...order,
    });
  };

  return (
    <div
      className={clsx(
        'flex px-4 pt-4 items-center fixed bottom-4 left-0 w-full h-32 gap-6',
        FOOTER_PATHS.includes(pathname) ? 'justify-center' : 'justify-end'
      )}
    >
      {FOOTER_PATHS.includes(pathname) && (
        <div className='flex justify-between items-center gap-4 bg-[#F5F5F5] w-[80%] h-full rounded-xl '>
          <div className='flex items-center gap-2 h-full'>
            <button
              onClick={() => setPage(page - 1)}
              disabled={page === 0}
              className={clsx(
                'text-white h-full rounded-tl-xl rounded-bl-xl px-1',
                page === 0 ? 'bg-subContent' : 'bg-secondary'
              )}
            >
              {'<'}
            </button>
          </div>
          <div className='grid grid-cols-4 gap-2 w-full pl-2'>
            {cartList[page]?.map((item) => (
              <Item
                key={item.cartId}
                cartId={item.cartId}
                imageUrl={item.imageUrl}
                name={item.name}
                quantity={item.quantity}
                onIncrease={() => handleIncrease(item.cartId)}
                onDecrease={() => handleDecrease(item.cartId)}
                onRemove={() => handleRemove(item.cartId)}
              />
            ))}
          </div>
          <button
            onClick={() => setPage(page + 1)}
            disabled={page === cartList.length - 1 || cartList.length === 0}
            className={clsx(
              'text-white h-full rounded-tr-xl rounded-br-xl px-1',
              page === cartList.length - 1 || cartList.length === 0
                ? 'bg-subContent'
                : 'bg-secondary'
            )}
          >
            {'>'}
          </button>
        </div>
      )}
      {recordingMethod === 'pitch' && (
        <PitchDetector
          ref={pitchDetectorRef}
          onRecognitionResult={handleRecognitionResult}
          setRecordingMethod={setRecordingMethod}
          onRecordStart={() => {
            const recordButton = document.querySelector(
              'button[aria-label="Record"]'
            );
            if (recordButton) {
              recordButton.dispatchEvent(new MouseEvent('mousedown'));
            }
          }}
          onRecordStop={() => {
            const recordButton = document.querySelector(
              'button[aria-label="Record"]'
            );
            if (recordButton) {
              recordButton.dispatchEvent(new MouseEvent('mouseup'));
            }
          }}
          onPreBufferUpdate={(buffer) => {
            recordButtonRef.current?.updatePreBuffer(buffer);
          }}
        />
      )}
      <RecordButton
        ref={recordButtonRef}
        onRecognitionResult={handleRecognitionResult}
        setRecordingMethod={setRecordingMethod}
        recordingMethod={recordingMethod}
      />
    </div>
  );
};

export default Footer;
