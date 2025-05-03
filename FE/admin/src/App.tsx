import { Route, Routes } from 'react-router-dom';

import Layout from '@/components/layout';
import MSWInit from '@/components/common/MSWinit';

import Statistics from '@/pages/Statistics';
import Login from '@/pages/Login';
import Menus from '@/pages/Menus';

function App() {
  return (
    <>
      <Routes>
        <Route element={<Layout />}>
          <Route path='/' element={<Statistics />} />
          <Route path='/menus' element={<Menus />} />
        </Route>
        <Route path='/login' element={<Login />} />
      </Routes>
      <MSWInit />
    </>
  );
}

export default App;
