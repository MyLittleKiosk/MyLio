import { Link, Outlet } from 'react-router-dom';

const OrderLayout = () => {
  return (
    // 배경 색은 추후 변경 예정
    <div className='flex flex-col h-dvh bg-gradient-to-b from-primary to-white justify-between'>
      <nav>
        <ul>
          <li>
            <Link to='/kiosk/main'>MAIN</Link>
          </li>
          <li>
            <Link to='/kiosk/order'>ORDER</Link>
          </li>
          <li>
            <Link to='/kiosk/detail'>DETAIL</Link>
          </li>
          <li>
            <Link to='/kiosk/search'>Search</Link>
          </li>
          <li>
            <Link to='/kiosk/pay'>PAY</Link>
          </li>
          <li>
            <Link to='/kiosk/select-pay'>SELECT PAY</Link>
          </li>
          <li>
            <Link to='/kiosk/confirm'>CONFIRM</Link>
          </li>
        </ul>
      </nav>
      <main className='h-[65%] rounded-t-xl bg-white shadow-t-2xl flex flex-col justify-center items-center'>
        <Outlet />
      </main>
    </div>
  );
};

export default OrderLayout;
