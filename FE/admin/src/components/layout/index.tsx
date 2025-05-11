import { Outlet, useNavigate } from 'react-router-dom';
import SideBar from './SideBar';
import { useGetRole } from '@/service/queries/user';
import { useEffect } from 'react';
import { useUserStore } from '@/stores/useUserStore';
const Layout = () => {
  const { data: role, isLoading, isError } = useGetRole();
  const { setUser } = useUserStore();
  const navigate = useNavigate();
  useEffect(() => {
    if (isError) {
      navigate('/login');
    }
  }, [isError]);
  useEffect(() => {
    if (!isLoading && role) {
      setUser(role);
    }
  }, [isLoading, role]);
  return (
    <div className='flex w-full h-full'>
      <SideBar />
      <Outlet />
    </div>
  );
};

export default Layout;
