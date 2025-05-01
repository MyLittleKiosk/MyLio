import { Outlet } from 'react-router-dom';
import SideBar from './SideBar';

const Layout = () => {
  return (
    <div className='flex w-full h-dvh'>
      <SideBar />
      <Outlet />
    </div>
  );
};

export default Layout;
