import { Route, Routes } from 'react-router-dom';

import MSWInit from '@/components/common/MSWInit';
import Layout from '@/components/layout';

import Login from '@/pages/Login';
import Menus from '@/pages/Menus';
import Kiosk from '@/pages/Kiosk';
import Statistics from '@/pages/Statistics';
import Accounts from '@/pages/Accounts';
import Orders from '@/pages/Orders';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';

function App() {
  const [queryClient] = React.useState(() => new QueryClient());
  return (
    <>
      <QueryClientProvider client={queryClient}>
        <Routes>
          <Route element={<Layout />}>
            <Route path='/' element={<Statistics />} />
            <Route path='/menus' element={<Menus />} />
            <Route path='/kiosks' element={<Kiosk />} />
            <Route path='/accounts' element={<Accounts />} />
            <Route path='/orders' element={<Orders />} />
          </Route>
          <Route path='/login' element={<Login />} />
        </Routes>
      </QueryClientProvider>
      <MSWInit />
    </>
  );
}

export default App;
