import { DEFAULT_COMMENT } from '@/datas/COMMENT';
import Main from '@/pages/Main';
import Footer from '@/pages/OrderLayout/Footer';
import { useOrderRequest } from '@/service/queries/order';
import { useLogout, useRefresh } from '@/service/queries/user';
import useOrderStore from '@/stores/useOrderStore';
import clsx from 'clsx';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom';

const OrderLayout = () => {
  const { pathname } = useLocation();
  const [userChat, setUserChat] = useState<string>('');
  const { order, resetOrder, setOrder } = useOrderStore();
  const { mutate: orderRequest, isPending } = useOrderRequest();
  const { mutate: logout } = useLogout();
  const { mutate: refresh } = useRefresh();
  const navigate = useNavigate();
  // const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const kioskId = localStorage.getItem('kioskId');
    if (!kioskId) {
      navigate('/');
    } else {
      refresh();
    }
  }, [navigate]);

  function handleLogout() {
    logout();
  }

  function handleRecognitionResult(text: string) {
    setUserChat(text);
    console.log('Recognition Result:', text);
    console.log('Current Order State:', order);

    // order 상태를 직접 업데이트하지 않고 API 요청만 보냄
    orderRequest({
      text: text,
      screenState: order.screenState,
      language: 'KR',
      sessionId: order.sessionId,
      cart: order.cart,
      contents: order.contents,
      payment: order.payment,
      storeId: order.storeId,
    });
  }

  function handleSessionReset() {
    resetOrder();
    orderRequest({
      text: '',
      screenState: 'MAIN',
      language: 'KR',
      sessionId: null,
      cart: [],
      contents: order.contents,
      payment: order.payment,
      storeId: order.storeId,
    });
    window.location.reload();
  }

  function handleTopLeftClick() {
    handleSessionReset();
  }

  function handleTopRightClick() {
    handleLogout();
  }

  function handleCartClick() {
    if (order.cart.length > 0) {
      handleRecognitionResult('장바구니 보여줘');
    } else {
      setOrder({
        ...order,
        reply: '장바구니가 비어있습니다.',
      });
    }
  }

  // function testHandleRecognitionResult() {
  //   handleRecognitionResult(inputRef.current?.value || '');
  // }

  const [isLargeFont, setIsLargeFont] = useState(false);

  function handleTopCenterClick() {
    setIsLargeFont(!isLargeFont);
  }

  useEffect(() => {
    const root = document.documentElement;

    if (isLargeFont) {
      root.classList.add('large-font');
    } else {
      root.classList.remove('large-font');
    }
  }, [isLargeFont]);

  return (
    // 배경 색은 추후 변경 예정
    <div
      className={clsx(
        'flex flex-col h-dvh bg-gradient-to-b from-secondary to-white justify-between'
      )}
    >
      <div
        className='fixed top-10 left-0 w-20 h-20 z-20 cursor-pointer'
        onClick={handleTopLeftClick}
      />

      <div className='flex fixed top-0 left-2 w-24 z-20 cursor-pointer items-center'>
        <div
          className={clsx(
            'w-[150px] font-preBold  bg-white border-2 rounded-full px-2 py-1',
            isLargeFont
              ? 'border-content text-content text-xs'
              : 'border-primary text-primary text-lg'
          )}
        >
          <Link className='text-center font-preSemiBold' to='/kiosk'>
            홈
          </Link>
        </div>
        <button
          onClick={handleTopCenterClick}
          className='flex flex-col items-start justify-center w-full rounded-lg p-2'
        >
          <span
            className={clsx(
              'w-[150px] font-preSemiBold  bg-white border-2 rounded-full p-1',
              isLargeFont
                ? 'border-content text-content text-xs'
                : 'border-primary text-primary text-lg'
            )}
          >
            {isLargeFont ? '작은 글자' : '큰 글자'}
          </span>
        </button>
        <button
          onClick={handleCartClick}
          className='flex flex-col items-start justify-center w-full rounded-lg'
        >
          <span
            className={clsx(
              'w-[200px] font-preSemiBold  bg-white border-2 rounded-full p-1',
              isLargeFont
                ? 'border-content text-content text-xs'
                : 'border-primary text-primary text-lg'
            )}
          >
            장바구니
          </span>
        </button>
      </div>

      <div
        className='fixed top-0 right-0 w-20 h-20 z-20 cursor-pointer'
        onClick={handleTopRightClick}
      />
      <header
        className={clsx(
          'flex justify-center items-center relative',
          pathname === '/kiosk' ? 'h-full' : 'h-1/3'
        )}
      >
        <Main
          userChat={userChat}
          gptChat={order.reply ? order.reply : DEFAULT_COMMENT}
          isPending={isPending}
        />
      </header>
      <motion.main
        className='rounded-t-xl bg-white  shadow-t-2xl flex flex-col justify-center items-center'
        initial={{ y: '100%', height: 0 }}
        animate={{
          y: pathname === '/kiosk' ? '100%' : 0,
          height: pathname === '/kiosk' ? 0 : '66.666667%',
        }}
        transition={{
          type: 'spring',
          duration: 0.7,
          damping: 25,
          stiffness: 200,
        }}
      >
        <Outlet />
      </motion.main>
      <Footer
        handleRecognitionResult={handleRecognitionResult}
        pathname={pathname}
      />
    </div>
  );
};

export default OrderLayout;
