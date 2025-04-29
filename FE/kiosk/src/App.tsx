import Clova from '@/pages/Clova';
import Login from '@/pages/Login';
import { BrowserRouter, Outlet, Route, Routes } from 'react-router-dom';
import './App.css';
import MSWInit from './components/common/MSWInit';

function App() {
  return (
    <>
      <MSWInit />
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<Login />} />
          <Route path='/kiosk' element={<Outlet />}>
            <Route index element={<div>홈페이지</div>} />
            <Route path='clova' element={<Clova />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
