import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

import LOGO from '@/assets/images/Character_HAo.png';
import IconBack from '@/assets/icons/IconBack';

import { ADMIN_NAVLIST, SUPERADMIN_NAVLIST } from '@/datas/sideBarList';

const SideBar = () => {
  //임시 데이터
  //추후 로그인 구현 시 수정 필요
  const ISSUPERADMIN: boolean = false;
  const LOGIN = '관리자';
  const VERSION = '1.0.0';
  const AUTHORITY = '일반관리자';

  const [isSideBarOpen, setIsSideBarOpen] = useState(true);

  // 사이드바 너비 조정 애니메이션 완료 여부
  const [isWidthAnimationComplete, setIsWidthAnimationComplete] =
    useState(true);

  useEffect(() => {
    if (!isSideBarOpen) {
      setIsWidthAnimationComplete(false);
    }
  }, [isSideBarOpen]);

  return (
    <motion.nav
      initial={false}
      layout
      animate={{ width: isSideBarOpen ? '180px' : '70px' }}
      transition={{
        width: { duration: 1, ease: 'easeInOut' },
        layout: { duration: 1, ease: 'easeInOut' },
      }}
      onAnimationComplete={() => {
        if (isSideBarOpen) {
          setIsWidthAnimationComplete(true);
        }
      }}
      className={`p-2 h-dvh flex flex-col`}
    >
      <header className='min-h-[50px] h-[8%] flex justify-between items-center gap-2 font-preBold text-lg text-primary'>
        <div className='h-full flex items-center gap-2 min-w-0'>
          <div className='w-8 flex-shrink-0'>
            <img src={LOGO} alt='logo' className='w-full h-full' />
          </div>
          {isWidthAnimationComplete && (
            <motion.h1
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.125 }}
              className='truncate'
            >
              MyLio
            </motion.h1>
          )}
        </div>
        <div className='ml-4 w-5 h-5'>
          <IconBack
            className={`text-content hover:bg-gray-100 rounded-md cursor-pointer ${
              isSideBarOpen ? '' : 'rotate-180'
            }`}
            onClick={() => setIsSideBarOpen(!isSideBarOpen)}
          />
        </div>
      </header>
      <hr className='w-full' />
      <section className='flex flex-col h-[80%] min-h-[120px]'>
        {!ISSUPERADMIN && (
          <ul className='pt-2 flex flex-col gap-1 text-xs font-preMedium'>
            {ADMIN_NAVLIST.map((item) => (
              <Link key={item.title} to={item.link}>
                <li className='flex items-center hover:bg-gray-100 rounded-md px-2 py-1'>
                  <div className='w-5 h-5 flex items-center justify-center'>
                    <item.icons width={20} height={20} />
                  </div>
                  <div className='ml-4'>
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
        {ISSUPERADMIN && (
          <ul className='pt-2 flex flex-col gap-1 text-xs font-preMedium'>
            {SUPERADMIN_NAVLIST.map((item) => (
              <Link key={item.title} to={item.link}>
                <li className='flex items-center hover:bg-gray-100 rounded-md px-2 py-1'>
                  <div className='w-5 h-5'>
                    <item.icons width={20} height={20} />
                  </div>
                  <div className='ml-4'>
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

      {isWidthAnimationComplete && <hr className='w-full' />}

      {isWidthAnimationComplete && (
        <footer
          className={`h-[10%] min-h-[80px] font-preMedium text-xs text-content p-2 flex flex-col justify-center gap-1`}
        >
          <p>로그인 : {LOGIN}</p>
          <p>버전 : {VERSION}</p>
          <p>권한 : {AUTHORITY}</p>
        </footer>
      )}
    </motion.nav>
  );
};

export default SideBar;
