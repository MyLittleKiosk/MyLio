import { PaginationResponse, Response } from '@/types/apiResponse';
import { MenuDetailGetType, MenuResponseType } from '@/types/menus';

const MENU_LIST: Response<PaginationResponse<MenuResponseType>> = {
  success: true,
  data: {
    content: [
      {
        menuId: 1,
        imageUrl:
          'https://ecimg.cafe24img.com/pg299b34409484036/baekih1001/web/product/big/20230613/9212adc2773009a8a949db20f147de69.jpg',
        nameKr: '아메리카노',
        nameEn: 'americano',
        category: '커피',
        storeName: 'MaLio 강남점',
        description: '어우 써!',
        price: 2000,
        status: '판매',
        tags: ['인기', '여름'],
      },
      {
        menuId: 2,
        imageUrl:
          'https://www.biz-con.co.kr/upload/images/202209/400_20220913183408720_%EC%B9%B4%ED%8E%98%EB%9D%BC%EB%96%BC-ICE.jpg',
        nameKr: '카페라떼',
        nameEn: 'latte',
        category: '커피',
        storeName: 'MaLio 강남점',
        description: '우유 최고!',
        price: 5000,
        status: '판매',
        tags: ['인기', '우유'],
      },
      {
        menuId: 3,
        imageUrl:
          'https://www.biz-con.co.kr/upload/images/202209/400_20220913183408720_%EC%B9%B4%ED%8E%98%EB%9D%BC%EB%96%BC-ICE.jpg',
        nameKr: '카페라떼',
        nameEn: 'latte',
        category: '커피',
        storeName: 'MaLio 강남점',
        description: '우유 최고!',
        price: 5000,
        status: '판매',
        tags: ['인기', '우유'],
      },
      {
        menuId: 4,
        imageUrl:
          'https://www.biz-con.co.kr/upload/images/202209/400_20220913183408720_%EC%B9%B4%ED%8E%98%EB%9D%BC%EB%96%BC-ICE.jpg',
        nameKr: '카페라떼',
        nameEn: 'latte',
        category: '커피',
        storeName: 'MaLio 강남점',
        description: '우유 최고!',
        price: 5000,
        status: '판매',
        tags: ['인기', '우유'],
      },
      {
        menuId: 5,
        imageUrl:
          'https://www.biz-con.co.kr/upload/images/202209/400_20220913183408720_%EC%B9%B4%ED%8E%98%EB%9D%BC%EB%96%BC-ICE.jpg',
        nameKr: '카페라떼',
        nameEn: 'latte',
        category: '커피',
        storeName: 'MaLio 강남점',
        description: '우유 최고!',
        price: 5000,
        status: '판매',
        tags: ['인기', '우유'],
      },
      {
        menuId: 6,
        imageUrl:
          'https://www.biz-con.co.kr/upload/images/202209/400_20220913183408720_%EC%B9%B4%ED%8E%98%EB%9D%BC%EB%96%BC-ICE.jpg',
        nameKr: '카페라떼',
        nameEn: 'latte',
        category: '커피',
        storeName: 'MaLio 강남점',
        description: '우유 최고!',
        price: 5000,
        status: '판매',
        tags: ['인기', '우유'],
      },
    ],
    pageNumber: 1,
    totalPages: 0,
    totalElements: 0,
    pageSize: 10,
    first: true,
    last: true,
  },
  timestamp: '2025-05-07T07:19:44.096473427',
};

const MENU_BY_ID: Response<MenuDetailGetType> = {
  success: true,
  data: {
    menuInfo: {
      menuId: 1,
      imageUrl: 'https://mylio',
      nameKr: '아이스 아메리카노',
      nameEn: 'ice americano',
      categoryId: 1,
      storeName: 'MaLio 강남점',
      description: 'MaLio 강남점',
      price: 2000,
      status: '판매',
    },
    tags: [
      {
        tagId: 1,
        tagKr: '달달해요',
        tagEn: 'sweet',
      },
    ],
    nutritionInfo: [
      {
        nutritionId: 1,
        nutritionName: '단백질',
        nutritionValue: 12,
        nutritionType: 'g',
      },
    ],
    ingredientInfo: [
      {
        menuIngredientId: 1,
        ingredientId: 2,
        ingredientNameKr: '우유',
        ingredientNameEn: 'milk',
      },
    ],
    optionInfo: [
      {
        menuOptionId: 1,
        optionId: 2,
        optionNameKr: '사이즈',
        optionNameEn: 'size',
        optionValue: 'S',
        additionalPrice: 500,
        required: true,
      },
    ],
  },
  timestamp: '2025-05-15T07:12:06.555Z',
};

export { MENU_LIST, MENU_BY_ID };
