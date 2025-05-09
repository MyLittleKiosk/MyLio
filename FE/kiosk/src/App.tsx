import MSWInit from '@/components/common/MSWInit';
import Clova from '@/pages/Clova';
import Confirm from '@/pages/Confirm';
import Detail from '@/pages/Detail';
import Login from '@/pages/Login';
import Menus from '@/pages/Menus';
import Order from '@/pages/Order';
import OrderLayout from '@/pages/OrderLayout';
import Pay from '@/pages/Pay';
import SelectPay from '@/pages/SelectPay';
import { Route, Routes } from 'react-router-dom';
import './App.css';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

function App() {
  return (
    <>
      <QueryClientProvider client={queryClient}>
        <MSWInit />
        <Routes>
          <Route path='/' element={<Login />} />
          <Route path='/clova' element={<Clova />} />
          <Route path='/kiosk' element={<OrderLayout />}>
            <Route path='search' element={<Menus />} />
            <Route path='order' element={<Order />} />
            <Route path='pay' element={<Pay />} />
            <Route path='select-pay' element={<SelectPay />} />
            <Route path='confirm' element={<Confirm />} />
            <Route path='detail' element={<Detail />} />
          </Route>
        </Routes>
      </QueryClientProvider>
    </>
  );
}

export default App;
