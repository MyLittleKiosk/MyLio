import IconStatistic from '@/assets/icons/IconStatistic';
import IconMenuList from '@/assets/icons/IconMenuList';
import IconCart from '@/assets/icons/IconCart';
import IconKiosk from '@/assets/icons/IconKiosk';
import IconAccount from '@/assets/icons/IconAccount';
import IconNutrient from '@/assets/icons/IconNutrient';
import IconIngredient from '@/assets/icons/IconIngredient';

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
