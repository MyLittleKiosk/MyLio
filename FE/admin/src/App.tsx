import { Route, Routes } from 'react-router-dom';
import Layout from './components/layout';
import Statistics from './pages/statistics';
import Login from './pages/login';

function App() {
  return (
    <>
      <Routes>
        <Route element={<Layout />}>
          <Route path='/' element={<Statistics />} />
        </Route>
        <Route path='/login' element={<Login />} />
      </Routes>
    </>
  );
}

export default App;
