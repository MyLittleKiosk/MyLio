import IconAccount from '@/assets/icons/IconAccount';
import IconCart from '@/assets/icons/IconCart';
import IconIngredient from '@/assets/icons/IconIngredient';
import IconKiosk from '@/assets/icons/IconKiosk';
import IconMenuList from '@/assets/icons/IconMenuList';
import IconNutrient from '@/assets/icons/IconNutrient';
import IconPerson from '@/assets/icons/IconPerson';
import IconStatistic from '@/assets/icons/IconStatistic';

const ADMIN_NAVLIST = [
  {
    icons: IconStatistic,
    title: '통계',
    link: '/',
  },
  {
    icons: IconMenuList,
    title: '메뉴 관리',
    link: '/menus',
  },
  {
    icons: IconCart,
    title: '주문 관리',
    link: '/orders',
  },
  {
    icons: IconKiosk,
    title: '키오스크 관리',
    link: '/kiosks',
  },
  {
    icons: IconPerson,
    title: '마이페이지',
    link: '/my',
  },
];

const SUPERADMIN_NAVLIST = [
  {
    icons: IconAccount,
    title: '계정 관리',
    link: '/accounts',
  },
  {
    icons: IconIngredient,
    title: '원재료 관리',
    link: '/ingredients',
  },
  {
    icons: IconNutrient,
    title: '영양소 관리',
    link: '/nutrients',
  },
];

export { ADMIN_NAVLIST, SUPERADMIN_NAVLIST };
