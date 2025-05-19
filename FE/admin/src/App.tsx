import { Route, Routes } from 'react-router-dom';

import Error from '@/components/common/Error';
import Layout from '@/components/layout';

import Accounts from '@/pages/Accounts';
import Ingredient from '@/pages/Ingredient';
import Kiosk from '@/pages/Kiosk';
import Login from '@/pages/Login';
import Menus from '@/pages/Menus';
import My from '@/pages/My';
import Nutrients from '@/pages/Nutrients';
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
          <Route path='/ingredients' element={<Ingredient />} />
          <Route path='/nutrients' element={<Nutrients />} />
        </Route>
        <Route path='/login' element={<Login />} />
        <Route path='*' element={<Error />} />
      </Routes>
      {/* <MSWInit /> */}
    </QueryClientProvider>
  );
}

export default App;
