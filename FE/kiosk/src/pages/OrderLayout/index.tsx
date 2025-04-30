import { Link, Outlet } from 'react-router-dom';

const OrderLayout = () => {
  return (
    <div>
      <nav>
        <ul>
          <li>
            <Link to='/kiosk/main'>MAIN</Link>
          </li>
          <li>
            <Link to='/kiosk/order'>ORDER</Link>
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
      <main>
        <Outlet />
      </main>
    </div>
  );
};

export default OrderLayout;
