import { Outlet } from 'react-router-dom';
import SideBar from './SideBar';

const Layout = () => {
  return (
    <div className='flex w-full h-full'>
      <SideBar />
      <Outlet />
    </div>
  );
};

export default Layout;
