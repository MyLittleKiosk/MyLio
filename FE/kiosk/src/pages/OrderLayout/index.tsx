import clsx from 'clsx';
import { motion } from 'framer-motion';
import { useEffect, useRef, useState } from 'react';
import { DEFAULT_COMMENT } from '@/datas/COMMENT';
import Main from '@/pages/Main';
import Footer from '@/pages/OrderLayout/Footer';
import { useLogout, useRefresh } from '@/service/queries/user';
import useOrderStore from '@/stores/useOrderStore';
import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom';
import { useOrderRequest } from '@/service/queries/order';
import useConsecutiveClick from '@/hooks/useConsecutiveClick';

const OrderLayout = () => {
  const { pathname } = useLocation();
  const [userChat, setUserChat] = useState<string>('');
  const { order, resetOrder } = useOrderStore();
  const { mutate: orderRequest, isPending } = useOrderRequest();
  const { mutate: logout } = useLogout();
  const { mutate: refresh } = useRefresh();
  const navigate = useNavigate();
  const inputRef = useRef<HTMLInputElement>(null);

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

  const handleTopLeftClick = useConsecutiveClick({
    onSuccess: handleSessionReset,
  });

  const handleTopRightClick = useConsecutiveClick({
    onSuccess: handleLogout,
  });

  function testHandleRecognitionResult() {
    handleRecognitionResult(inputRef.current?.value || '');
  }

  const [isLargeFont, setIsLargeFont] = useState(false);

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
        className='fixed top-0 left-0 w-20 h-20 z-20 cursor-pointer'
        onClick={handleTopLeftClick}
      />
      <div
        className='fixed top-0 right-0 w-20 h-20 z-20 cursor-pointer'
        onClick={handleTopRightClick}
      />
      <div className='flex justify-center items-center z-10 fixed top-0 left-0 w-full h-[100px] flex-wrap'>
        <ul className='flex justify-center items-center gap-4 rounded-xl p-4'>
          <li>
            <Link to='/kiosk'>홈</Link>
          </li>
          <li>
            <Link to='search'>검색</Link>
          </li>
          <li>
            <Link to='order'>주문</Link>
          </li>
          <li>
            <Link to='select-pay'>결제 수단</Link>
          </li>
          <li>
            <Link to='pay'>결제</Link>
          </li>
          <li>
            <Link to='confirm'>확인</Link>
          </li>
          <li>
            <button onClick={() => setIsLargeFont(!isLargeFont)}>
              {isLargeFont ? '작게' : '크게'}
            </button>
          </li>
          <li>
            <Link to='detail'>상세</Link>
          </li>
        </ul>
        <div className='flex gap-4'>
          <div className='flex gap-2 h-full'>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                testHandleRecognitionResult();
              }}
              className='flex gap-2 h-full'
            >
              <input type='text' ref={inputRef} />
              <button type='submit'>전송</button>
            </form>
          </div>
        </div>
      </div>
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
