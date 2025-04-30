import { Route, Routes } from 'react-router-dom';
import Layout from './components/layout';
import Statistics from './pages/Statistics';
import Login from './pages/Login';
import MSWInit from '@components/common/MSWinit';

function App() {
  return (
    <>
      <Routes>
        <Route element={<Layout />}>
          <Route path='/' element={<Statistics />} />
        </Route>
        <Route path='/login' element={<Login />} />
      </Routes>
      <MSWInit />
    </>
  );
}

export default App;
