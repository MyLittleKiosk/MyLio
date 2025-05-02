import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import Login from '@/pages/Login';
import MSWInit from '@/components/common/MSWInit';
import Confirm from '@/pages/Confirm';
import Order from '@/pages/Order';
import SelectPay from '@/pages/SelectPay';
import Detail from '@/pages/Detail';
import Pay from '@/pages/Pay';
import Main from '@/pages/Main';
import OrderLayout from '@/pages/OrderLayout';
import Menus from '@/pages/Menus';
function App() {
  return (
    <>
      <MSWInit />
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<Login />} />
          <Route path='/kiosk' element={<OrderLayout />}>
            <Route path='main' element={<Main />} />
            <Route path='search' element={<Menus />} />
            <Route path='order' element={<Order />} />
            <Route path='pay' element={<Pay />} />
            <Route path='select-pay' element={<SelectPay />} />
            <Route path='confirm' element={<Confirm />} />
            <Route path='detail' element={<Detail />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
