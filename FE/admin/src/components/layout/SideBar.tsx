import { Link } from 'react-router-dom';

import LOGO from '../../assets/images/Character_HAo.png';
import IconStatistic from '../../assets/icons/IconStatistic';
import IconMenuList from '../../assets/icons/IconMenuList';
import IconCart from '../../assets/icons/IconCart';
import IconKiosk from '../../assets/icons/IconKiosk';
import IconAccount from '../../assets/icons/IconAccount';
import IconNutrient from '../../assets/icons/IconNutrient';
import IconIngredient from '../../assets/icons/IconIngredient';
import IconBack from '../../assets/icons/IconBack';

const adminNavList = [
  {
    icons: IconStatistic,
    title: '통계',
    link: '/',
  },
  {
    icons: IconMenuList,
    title: '메뉴 관리',
    link: '/',
  },
  {
    icons: IconCart,
    title: '주문 관리',
    link: '/',
  },
  {
    icons: IconKiosk,
    title: '키오스크 관리',
    link: '/',
  },
];

const superAdminNavList = [
  {
    icons: IconAccount,
    title: '계정 관리',
    link: '/',
  },
  {
    icons: IconIngredient,
    title: '원재료 관리',
    link: '/',
  },
  {
    icons: IconNutrient,
    title: '영양소 관리',
    link: '/',
  },
];

const SideBar = () => {
  const ISADMIN: boolean = true;
  return (
    <nav className='w-[30%] p-2 h-dvh flex flex-col'>
      <header className='h-[8%] flex justify-between items-center gap-2 font-preBold text-md'>
        <div className='flex items-center gap-2'>
          <img src={LOGO} alt='logo' className='w-10 h-10' />
          <h1 className=''>MyLio</h1>
        </div>
        <IconBack
          width={16}
          height={16}
          onClick={() => {}}
          className='text-black hover:bg-gray-100 rounded-md cursor-pointer'
        />
      </header>
      <hr className='w-full' />
      <div className='flex flex-col h-[70%]'>
        <ul className='pt-2 flex flex-col gap-1 text-xs font-preMedium'>
          {adminNavList.map((item) => (
            <Link key={item.title} to={item.link}>
              <li className='flex gap-2 items-center hover:bg-gray-100 rounded-md px-2 py-1'>
                <item.icons width={20} height={20} />
                <p>{item.title}</p>
              </li>
            </Link>
          ))}
        </ul>
        {ISADMIN && (
          <div className='flex flex-col pt-4'>
            <p className='px-2 text-xs font-preSemiBold text-content'>
              슈퍼어드민 메뉴
            </p>
            <ul className='h-[70%] pt-2 flex flex-col gap-1 text-xs font-preMedium'>
              {superAdminNavList.map((item) => (
                <Link key={item.title} to={item.link}>
                  <li className='flex gap-2 items-center hover:bg-gray-100 rounded-md px-2 py-1'>
                    <item.icons width={18} height={18} />
                    <p>{item.title}</p>
                  </li>
                </Link>
              ))}
            </ul>
          </div>
        )}
      </div>

      <hr className='w-full' />
      <footer className='h-[20%] font-preMedium text-xs text-content p-2 flex flex-col gap-1'>
        <p>로그인 : 관리자</p>
        <p>버전 : 1.0.0</p>
        <p>권한 : 일반관리자</p>
        <p>토글</p>
      </footer>
    </nav>
  );
};

export default SideBar;
