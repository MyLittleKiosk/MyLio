import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

import LOGO from '@/assets/images/Character_HAo.png';
import IconBack from '@/assets/icons/IconBack';

import { ADMIN_NAVLIST, SUPERADMIN_NAVLIST } from '@/datas/sideBarList';

const SideBar = () => {
  //임시 데이터
  //추후 로그인 구현 시 수정 필요
  const ISADMIN: boolean = true;
  const LOGIN = '관리자';
  const VERSION = '1.0.0';
  const AUTHORITY = '일반관리자';

  const [isSideBarOpen, setIsSideBarOpen] = useState(true);

  // 사이드바 너비 조정 애니메이션 완료 여부부
  const [isWidthAnimationComplete, setIsWidthAnimationComplete] =
    useState(false);

  useEffect(() => {
    if (!isSideBarOpen) {
      setIsWidthAnimationComplete(false);
    }
  }, [isSideBarOpen]);

  return (
    <motion.nav
      animate={{ width: isSideBarOpen ? '20%' : '80px' }}
      transition={{ duration: 0.2, ease: 'easeInOut' }}
      onAnimationComplete={() => {
        if (isSideBarOpen) {
          setIsWidthAnimationComplete(true);
        }
      }}
      className={`p-2 h-dvh flex flex-col`}
    >
      <header className='h-[8%] flex justify-between items-center gap-2 font-preBold text-lg text-primary'>
        <div className='flex items-center gap-2'>
          <div className='w-10 h-10'>
            <img src={LOGO} alt='logo' className='w-10 h-10' />
          </div>
          {isWidthAnimationComplete && (
            <motion.h1
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.125 }}
            >
              MyLio
            </motion.h1>
          )}
        </div>
        <IconBack
          width={16}
          height={16}
          onClick={() => setIsSideBarOpen(!isSideBarOpen)}
          className={`mr-2 text-black hover:bg-gray-100 rounded-md cursor-pointer transform transition-transform ${
            isSideBarOpen ? '' : 'rotate-180'
          }`}
        />
      </header>
      <hr className='w-full' />
      <section className='flex flex-col h-[80%]'>
        {!ISADMIN && (
          <ul className='pt-2 flex flex-col gap-1 text-xs font-preMedium'>
            {ADMIN_NAVLIST.map((item) => (
              <Link key={item.title} to={item.link}>
                <li className='flex items-center hover:bg-gray-100 rounded-md px-2 py-1'>
                  <div className='w-5 h-5'>
                    <item.icons width={20} height={20} />
                  </div>
                  <div className='overflow-hidden'>
                    {isSideBarOpen && (
                      <motion.p
                        initial={{ opacity: 0, y: 12 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.125 }}
                      >
                        {item.title}
                      </motion.p>
                    )}
                  </div>
                </li>
              </Link>
            ))}
          </ul>
        )}
        {ISADMIN && (
          <ul className='pt-2 flex flex-col gap-1 text-xs font-preMedium'>
            {SUPERADMIN_NAVLIST.map((item) => (
              <Link key={item.title} to={item.link}>
                <li className='flex items-center hover:bg-gray-100 rounded-md px-2 py-1'>
                  <div className='w-5 h-5'>
                    <item.icons width={20} height={20} />
                  </div>
                  <div className='ml-4 overflow-hidden'>
                    {isWidthAnimationComplete && (
                      <motion.p
                        initial={{ opacity: 0, y: 12 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.125 }}
                      >
                        {item.title}
                      </motion.p>
                    )}
                  </div>
                </li>
              </Link>
            ))}
          </ul>
        )}
      </section>

      <hr className='w-full' />
      {isWidthAnimationComplete && (
        <footer className='h-[10%] font-preMedium text-xs text-content p-2 flex flex-col gap-1'>
          <p>로그인 : {LOGIN}</p>
          <p>버전 : {VERSION}</p>
          <p>권한 : {AUTHORITY}</p>
        </footer>
      )}
    </motion.nav>
  );
};

export default SideBar;
