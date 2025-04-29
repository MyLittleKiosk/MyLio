import { BrowserRouter, Routes, Route, Outlet } from 'react-router-dom';
import './App.css';
import Login from '@/pages/Login';
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
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
