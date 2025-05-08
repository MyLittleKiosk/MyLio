import { Link, Outlet, useLocation } from 'react-router-dom';
import Main from '@/pages/Main';
import clsx from 'clsx';
import { motion } from 'framer-motion';

const OrderLayout = () => {
  const { pathname } = useLocation();
  return (
    // 배경 색은 추후 변경 예정
    <div className='flex flex-col h-dvh bg-gradient-to-b from-primary to-white justify-between'>
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
      </div>
      <header
        className={clsx(
          'flex justify-center items-center',
          pathname === '/kiosk' ? 'h-full' : 'h-1/3'
        )}
      >
        <Main userChat={''} gptChat={''} isRecording={false} volume={0} />
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
