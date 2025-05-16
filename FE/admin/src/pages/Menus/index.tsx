import { Suspense, useState } from 'react';
import { ErrorBoundary } from 'react-error-boundary';

import Modal from '@/components/common/Modal';
import Menu from '@/components/menus/Menu';
import Category from '@/components/menus/Category';
import Option from '@/components/menus/Option';
import AddMenuForm from '@/components/menus/AddMenuForm';
import Button from '@/components/common/Button';
import EditMenuForm from '@/components/menus/EditMenuForm';

import { MENU_NAV_LIST } from '@/datas/menuList';
import { NavItemType } from '@/types/menus';
import IconAdd from '@/assets/icons/IconAdd';
import Error from '@/components/common/Error';
import Loading from '@/components/common/Loading';

const Menus = () => {
  const [selectedNav, setSelectedNav] = useState<NavItemType>(MENU_NAV_LIST[0]);
  const [isAddMenuClicked, setIsAddMenuClicked] = useState(false);
  const [isEditMenuClicked, setIsEditMenuClicked] = useState(false);
  const [clickedMenuId, setClickedMenuId] = useState<number | null>(null);

  return (
    <>
      <section className='w-full h-full p-4 flex flex-col gap-2'>
        <div className='flex justify-between'>
          <h1 className='text-2xl font-preBold h-[5%]'>메뉴 목록</h1>
          <Button
            type='button'
            text='메뉴 추가'
            icon={<IconAdd fillColor='white' />}
            onClick={() => {
              setIsAddMenuClicked(true);
            }}
            className='w-[11%] items-center justify-center'
          />
        </div>

        {isAddMenuClicked ? (
          <AddMenuForm setIsAddMenuClicked={setIsAddMenuClicked} />
        ) : isEditMenuClicked ? (
          <EditMenuForm
            setIsEditMenuClicked={setIsEditMenuClicked}
            clickedMenuId={clickedMenuId as number}
          />
        ) : (
          <>
            <nav className='bg-subContent/50 rounded-md p-2 w-fit'>
              <ul className='flex items-center justify-center gap-2 text-sm font-preMedium'>
                {MENU_NAV_LIST.map((navItem) => {
                  return (
                    <li
                      id={navItem.title}
                      key={navItem.title}
                      onClick={() => setSelectedNav(navItem)}
                      className={`cursor-pointer hover:bg-white rounded-md px-2 py-1 ${
                        selectedNav.title === navItem.title && 'bg-white'
                      }`}
                    >
                      {navItem.title}
                    </li>
                  );
                })}
              </ul>
            </nav>
            <div className='w-full h-full'>
              <ErrorBoundary fallback={<Error />}>
                <Suspense fallback={<Loading />}>
                  {selectedNav.title === '메뉴' && (
                    <Menu
                      selectedNav={selectedNav}
                      setIsEditMenuClicked={setIsEditMenuClicked}
                      setClickedMenuId={setClickedMenuId}
                    />
                  )}
                  {selectedNav.title === '카테고리' && (
                    <Category selectedNav={selectedNav} />
                  )}
                  {selectedNav.title === '옵션' && (
                    <Option selectedNav={selectedNav} />
                  )}
                </Suspense>
              </ErrorBoundary>
            </div>
          </>
        )}
      </section>
      <Modal />
    </>
  );
};

export default Menus;
