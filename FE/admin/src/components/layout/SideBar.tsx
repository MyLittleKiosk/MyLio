import { Link } from 'react-router-dom';

import LOGO from '@/assets/images/Character_HAo.png';
import IconBack from '@/assets/icons/IconBack';

import { ADMIN_NAVLIST, SUPERADMIN_NAVLIST } from '@/datas/sideBarList';

interface SideBarProps {
  isSideBarOpen: boolean;
  setIsSideBarOpen: (isSideBarOpen: boolean) => void;
}

const SideBar = ({ isSideBarOpen, setIsSideBarOpen }: SideBarProps) => {
  //임시 데이터
  //추후 로그인 구현 시 수정 필요
  const ISADMIN: boolean = true;
  const LOGIN = '관리자';
  const VERSION = '1.0.0';
  const AUTHORITY = '일반관리자';

  return (
    <nav
      className={`${isSideBarOpen ? 'w-[20%]' : 'w-[80px]'} p-2 h-dvh flex flex-col`}
    >
      <header className='h-[8%] flex justify-between items-center gap-2 font-preBold text-lg text-primary'>
        <div className='flex items-center gap-2'>
          <img src={LOGO} alt='logo' className='w-10 h-10' />
          {isSideBarOpen && <h1>MyLio</h1>}
        </div>
        <IconBack
          width={16}
          height={16}
          onClick={() => setIsSideBarOpen(!isSideBarOpen)}
          className={`mr-2 text-black hover:bg-gray-100 rounded-md cursor-pointer transform ${
            isSideBarOpen ? '' : 'rotate-180'
          }`}
        />
      </header>
      <hr className='w-full' />
      <div className='flex flex-col h-[80%]'>
        {!ISADMIN && (
          <ul className='pt-2 flex flex-col gap-1 text-xs font-preMedium'>
            {ADMIN_NAVLIST.map((item) => (
              <Link key={item.title} to={item.link}>
                <li className='flex gap-2 items-center hover:bg-gray-100 rounded-md px-2 py-1'>
                  <item.icons width={20} height={20} />
                  {isSideBarOpen && <p>{item.title}</p>}
                </li>
              </Link>
            ))}
          </ul>
        )}
        {ISADMIN && (
          <ul className='pt-2 flex flex-col gap-1 text-xs font-preMedium'>
            {SUPERADMIN_NAVLIST.map((item) => (
              <Link key={item.title} to={item.link}>
                <li className='flex gap-2 items-center hover:bg-gray-100 rounded-md px-2 py-1'>
                  <item.icons width={18} height={18} />
                  {isSideBarOpen && <p>{item.title}</p>}
                </li>
              </Link>
            ))}
          </ul>
        )}
      </div>

      <hr className='w-full' />
      {isSideBarOpen && (
        <footer className='h-[10%] font-preMedium text-xs text-content p-2 flex flex-col gap-1'>
          <p>로그인 : {LOGIN}</p>
          <p>버전 : {VERSION}</p>
          <p>권한 : {AUTHORITY}</p>
        </footer>
      )}
    </nav>
  );
};

export default SideBar;
