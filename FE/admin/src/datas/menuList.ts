import { Menu, MenuList } from '@/types/menus';
import { Column } from '@/types/tableProps';

const MENU_COLUMNS: Column<Menu>[] = [
  {
    header: '이미지',
    accessor: 'image_url' as keyof Menu,
  },
  {
    header: '메뉴명',
    accessor: 'name_kr' as keyof Menu,
  },
  {
    header: '카테고리',
    accessor: 'category' as keyof Menu,
  },
  {
    header: '가격',
    accessor: 'price' as keyof Menu,
  },
  {
    header: '점포',
    accessor: 'store_name' as keyof Menu,
  },
  {
    header: '설명',
    accessor: 'description' as keyof Menu,
    className: 'px-4 py-3 text-sm font-preRegular max-w-xs truncate',
  },
  {
    header: '편집',
    accessor: 'edit' as keyof Menu,
  },
  {
    header: '삭제',
    accessor: 'delete' as keyof Menu,
  },
];

const MENU_LIST: MenuList = {
  content: [
    {
      menu_id: 1,
      image_url:
        'https://ecimg.cafe24img.com/pg299b34409484036/baekih1001/web/product/big/20230613/9212adc2773009a8a949db20f147de69.jpg',
      name_kr: '아메리카노',
      name_en: 'americano',
      category: '커피',
      store_name: 'MaLio 강남점',
      description: '어우 써!',
      price: 2000,
      status: '판매',
      tags: ['인기', '여름'],
    },
    {
      menu_id: 2,
      image_url:
        'https://www.biz-con.co.kr/upload/images/202209/400_20220913183408720_%EC%B9%B4%ED%8E%98%EB%9D%BC%EB%96%BC-ICE.jpg',
      name_kr: '카페라떼',
      name_en: 'latte',
      category: '커피',
      store_name: 'MaLio 강남점',
      description: '우유 최고!',
      price: 5000,
      status: '판매',
      tags: ['인기', '우유'],
    },
    {
      menu_id: 3,
      image_url:
        'https://www.biz-con.co.kr/upload/images/202209/400_20220913183408720_%EC%B9%B4%ED%8E%98%EB%9D%BC%EB%96%BC-ICE.jpg',
      name_kr: '카페라떼',
      name_en: 'latte',
      category: '커피',
      store_name: 'MaLio 강남점',
      description: '우유 최고!',
      price: 5000,
      status: '판매',
      tags: ['인기', '우유'],
    },
    {
      menu_id: 4,
      image_url:
        'https://www.biz-con.co.kr/upload/images/202209/400_20220913183408720_%EC%B9%B4%ED%8E%98%EB%9D%BC%EB%96%BC-ICE.jpg',
      name_kr: '카페라떼',
      name_en: 'latte',
      category: '커피',
      store_name: 'MaLio 강남점',
      description: '우유 최고!',
      price: 5000,
      status: '판매',
      tags: ['인기', '우유'],
    },
    {
      menu_id: 5,
      image_url:
        'https://www.biz-con.co.kr/upload/images/202209/400_20220913183408720_%EC%B9%B4%ED%8E%98%EB%9D%BC%EB%96%BC-ICE.jpg',
      name_kr: '카페라떼',
      name_en: 'latte',
      category: '커피',
      store_name: 'MaLio 강남점',
      description: '우유 최고!',
      price: 5000,
      status: '판매',
      tags: ['인기', '우유'],
    },
    {
      menu_id: 6,
      image_url:
        'https://www.biz-con.co.kr/upload/images/202209/400_20220913183408720_%EC%B9%B4%ED%8E%98%EB%9D%BC%EB%96%BC-ICE.jpg',
      name_kr: '카페라떼',
      name_en: 'latte',
      category: '커피',
      store_name: 'MaLio 강남점',
      description: '우유 최고!',
      price: 5000,
      status: '판매',
      tags: ['인기', '우유'],
    },
  ],
  page_number: 1,
  total_pages: 1,
  total_elements: 6,
  page_size: 10,
  first: true,
  last: true,
  error: null,
};

const MENU_NAV_LIST = [
  {
    title: '메뉴',
    columns: MENU_COLUMNS,
    data: MENU_LIST,
  },
  {
    title: '카테고리',
    columns: MENU_COLUMNS,
    data: MENU_LIST,
  },
  {
    title: '옵션',
    columns: MENU_COLUMNS,
    data: MENU_LIST,
  },
];
export { MENU_COLUMNS, MENU_LIST, MENU_NAV_LIST };
