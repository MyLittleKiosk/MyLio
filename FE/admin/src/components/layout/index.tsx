import { useAuthGuard } from '@/hooks/useAuthGuard'; // 새로 만든 훅 임포트
import { Outlet } from 'react-router-dom';

import Loading from '@/components/common/Loading';
import SideBar from '@/components/layout/SideBar';

const Layout = () => {
  const { isLoadingAuth } = useAuthGuard();

  // 초기 로딩 상태
  if (isLoadingAuth) {
    return <Loading />;
  }

  // 인증 및 권한 검사가 완료된 후 (문제가 있으면 훅 내부에서 리디렉션됨)
  return (
    <div className='flex w-full h-full'>
      <SideBar />
      <Outlet />
    </div>
  );
};

export default Layout;
