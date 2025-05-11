import { Route, Routes } from 'react-router-dom';

import MSWInit from '@/components/common/MSWInit';
import Layout from '@/components/layout';

import Accounts from '@/pages/Accounts';
import Kiosk from '@/pages/Kiosk';
import Login from '@/pages/Login';
import Menus from '@/pages/Menus';
import My from '@/pages/My';
import Orders from '@/pages/Orders';
import Statistics from '@/pages/Statistics';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

function App() {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <Routes>
        <Route element={<Layout />}>
          <Route path='/' element={<Statistics />} />
          <Route path='/menus' element={<Menus />} />
          <Route path='/kiosks' element={<Kiosk />} />
          <Route path='/accounts' element={<Accounts />} />
          <Route path='/orders' element={<Orders />} />
          <Route path='/my' element={<My />} />
        </Route>
        <Route path='/login' element={<Login />} />
      </Routes>
      <MSWInit />
    </QueryClientProvider>
  );
}

export default App;
