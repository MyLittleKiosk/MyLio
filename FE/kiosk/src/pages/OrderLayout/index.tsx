import clsx from 'clsx';
import { motion } from 'framer-motion';
import React, { useEffect, useRef, useState } from 'react';
import { DEFAULT_COMMENT } from '@/datas/COMMENT';
import Main from '@/pages/Main';
import Footer from '@/pages/OrderLayout/Footer';
import { useLogout, useRefresh } from '@/service/queries/user';
import useOrderStore from '@/stores/useOrderStore';
import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom';
import { useOrderRequest } from '@/service/queries/order';

const OrderLayout = () => {
  const { pathname } = useLocation();
  const [userChat] = useState<string>('');
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
  }
  function testHandleRecognitionResult() {
    handleRecognitionResult(inputRef.current?.value || '');
  }
  function pressEnter(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter') {
      testHandleRecognitionResult();
    }
  }

  return (
    // 배경 색은 추후 변경 예정
    <div className='flex flex-col h-dvh bg-gradient-to-b from-secondary to-white justify-between'>
      {/* 임시 네비게이터 */}
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
            <Link to='detail'>상세</Link>
          </li>
        </ul>
        <div className='flex gap-4'>
          <button onClick={handleLogout}>로그아웃</button>
          <button onClick={handleSessionReset}>세션 초기화</button>
          <div className='flex gap-2 h-full'>
            <input type='text' ref={inputRef} onKeyDown={pressEnter} />
            <button onClick={testHandleRecognitionResult}>전송</button>
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
        className='rounded-t-xl bg-white shadow-t-2xl flex flex-col justify-start items-center pt-5'
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
        order={order}
        handleRecognitionResult={handleRecognitionResult}
        pathname={pathname}
      />
    </div>
  );
};

export default OrderLayout;
