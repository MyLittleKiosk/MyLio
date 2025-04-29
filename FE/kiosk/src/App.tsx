import { BrowserRouter, Routes, Route, Outlet } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Outlet />}>
          <Route index element={<div>홈페이지</div>} />
          <Route path='login' element={<div>로그인 페이지</div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
