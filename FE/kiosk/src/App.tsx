import Clova from '@/pages/Clova';
import Confirm from '@/pages/Confirm';
import Detail from '@/pages/Detail';
import Login from '@/pages/Login';
import Menus from '@/pages/Menus';
import Order from '@/pages/Order';
import OrderLayout from '@/pages/OrderLayout';
import Pay from '@/pages/Pay';
import Success from '@/pages/Pay/Success';
import SelectPay from '@/pages/SelectPay';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Route, Routes } from 'react-router-dom';
import './App.css';
import PayLoading from './pages/Pay/PayLoading';
import Landing from './pages/Lading';
const queryClient = new QueryClient();

function App() {
  return (
    <>
      <QueryClientProvider client={queryClient}>
        {/* <MSWInit /> */}
        <Routes>
          <Route path='/' element={<Login />} />
          <Route path='/clova' element={<Clova />} />
          <Route path='/landing' element={<Landing />} />
          <Route path='/kiosk' element={<OrderLayout />}>
            <Route path='search' element={<Menus />} />
            <Route path='order' element={<Order />} />
            <Route path='pay' element={<Pay />} />
            <Route path='pay/loading' element={<PayLoading />} />
            <Route path='select-pay' element={<SelectPay />} />
            <Route path='confirm' element={<Confirm />} />
            <Route path='detail' element={<Detail />} />
          </Route>
          <Route path='/success' element={<Success />} />
        </Routes>
      </QueryClientProvider>
    </>
  );
}

export default App;
