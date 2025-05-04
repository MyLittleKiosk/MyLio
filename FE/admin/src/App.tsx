import { Route, Routes } from 'react-router-dom';

import MSWInit from '@/components/common/MSWInit';
import Layout from '@/components/layout';

import Login from '@/pages/Login';
import Menus from '@/pages/Menus';
import Statistics from '@/pages/Statistics';

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
