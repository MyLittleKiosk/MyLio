import { Response } from '@/types/apiResponse';
import { MenuList } from '@/types/menus';

const MENU_LIST: Response<MenuList> = {
  success: true,
  data: {
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
    total_pages: 0,
    total_elements: 0,
    page_size: 10,
    first: true,
    last: true,
  },
  timestamp: '2025-05-07T07:19:44.096473427',
};

export default MENU_LIST;
