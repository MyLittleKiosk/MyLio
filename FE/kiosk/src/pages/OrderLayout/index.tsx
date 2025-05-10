import { Link, Outlet, useLocation } from 'react-router-dom';
import Main from '@/pages/Main';
import clsx from 'clsx';
import { motion } from 'framer-motion';
import RecordButton from '@/components/Chat/RecordButton';
import { useState } from 'react';
import { useOrderRequest } from '@/service/queries/useOrderRequest';
import useOrderStore from '@/stores/useOrderStore';
import { DEFAULT_COMMENT } from '@/datas/COMMENT';
import { useLogout } from '@/service/queries/useLogout';
const OrderLayout = () => {
  const { pathname } = useLocation();
  const [userChat, setUserChat] = useState<string>('');
  const { order } = useOrderStore();
  const { mutate: orderRequest } = useOrderRequest();
  const { mutate: logout } = useLogout();
  const handleRecognitionResult = (text: string) => {
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
  };

  return (
    // 배경 색은 추후 변경 예정
    <div className='flex flex-col h-dvh bg-gradient-to-b from-primary to-white justify-between'>
      {/* 임시 네비게이터 */}
      <div className='flex justify-center items-center z-10 fixed top-20 left-0 w-full h-1/3'>
        <ul className='flex justify-center items-center gap-4 bg-white rounded-xl p-4'>
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
        <button onClick={() => logout(3)}>로그아웃</button>
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
        />
        <RecordButton onRecognitionResult={handleRecognitionResult} />
      </header>
      <motion.main
        className='rounded-t-xl bg-white shadow-t-2xl flex flex-col justify-center items-center'
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
    </div>
  );
};

export default OrderLayout;
