import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import SideBar from './SideBar';

const Layout = () => {
  const [isSideBarOpen, setIsSideBarOpen] = useState(false);
  return (
    <div className='flex w-full'>
      <SideBar
        isSideBarOpen={isSideBarOpen}
        setIsSideBarOpen={setIsSideBarOpen}
      />
      <Outlet />
    </div>
  );
};

export default Layout;
