import { http, HttpResponse } from 'msw';
import { userRole } from './dummies/user';

import { DUMMY_ACCOUNT_LIST } from '@/datas/Account';
import { AccountType } from '@/types/account';
import { PaginationResponse, Response } from '@/types/apiResponse';
import {
  CategorySalesRatioType,
  DailySalesStatisticsType,
  OrderSalesRatioType,
  PaymentSalesRatioType,
} from '@/types/statistics';
import { CATEGORY_LIST } from './dummies/category';
import { MENU_LIST, MENU_BY_ID } from './dummies/menu';
import DUMMY_MY_INFO from './dummies/my';
import { OPTION_LIST } from './dummies/option';
import {
  DUMMY_CATEGORY_SALES_BY_YEAR_2024,
  DUMMY_DAILY_SALES,
  DUMMY_ORDER_TYPES_BY_YEAR_2024,
  DUMMY_PAYMENTS_BY_YEAR_2024,
  DUMMY_SALES_BY_MONTH_2024_05,
  DUMMY_SALES_BY_MONTH_2025_08,
  DUMMY_SALES_BY_YEAR_2024,
  DUMMY_SALES_BY_YEAR_2025,
} from './dummies/statistics';
import { KIOSK_LIST } from '@/datas/kioskList';

const baseUrl = import.meta.env.VITE_PUBLIC_API_URL;

export const handlers = [
  http.get(`${baseUrl}/sales`, ({ request }) => {
    const url = new URL(request.url);
    const month = url.searchParams.get('month');
    const year = url.searchParams.get('year');
    console.log('month:', month, typeof month);
    console.log('year:', year, typeof year);
    if (month) {
      if (month === '5') {
        console.log('DUMMY_SALES_BY_MONTH_2024_05');
        return HttpResponse.json({ data: DUMMY_SALES_BY_MONTH_2024_05 });
      } else {
        console.log('DUMMY_SALES_BY_MONTH_2025_08');
        return HttpResponse.json({ data: DUMMY_SALES_BY_MONTH_2025_08 });
      }
    }
    if (year) {
      if (year === '2024') {
        console.log('DUMMY_SALES_BY_YEAR_2024');
        return HttpResponse.json({ data: DUMMY_SALES_BY_YEAR_2024 });
      } else if (year === '2025') {
        console.log('DUMMY_SALES_BY_YEAR_2025');
        return HttpResponse.json({ data: DUMMY_SALES_BY_YEAR_2025 });
      }
    }
    return HttpResponse.json({ data: DUMMY_SALES_BY_YEAR_2024 });
  }),

  http.get(`${baseUrl}/menus`, () => {
    return HttpResponse.json(MENU_LIST);
  }),

  http.get(`${baseUrl}/menus/:menuId`, () => {
    return HttpResponse.json(MENU_BY_ID);
  }),

  http.post(`${baseUrl}/menus`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.put(`${baseUrl}/menus/:menuId`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.get(`${baseUrl}/option`, () => {
    return HttpResponse.json(OPTION_LIST);
  }),

  http.post(`${baseUrl}/option`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.patch(`${baseUrl}/option/:optionId`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.delete(`${baseUrl}/option/:optionId`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.post(`${baseUrl}/option_detail/:optionId`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.patch(`${baseUrl}/option_detail/:optionDetailId`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.delete(`${baseUrl}/option_detail/:optionDetailId`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.get(`${baseUrl}/accounts/role`, () => {
    return HttpResponse.json(userRole);
  }),

  http.get(`${baseUrl}/sales/by_payment?year=2024`, () => {
    const responseData: Response<PaymentSalesRatioType[]> = {
      success: true,
      data: DUMMY_PAYMENTS_BY_YEAR_2024,
      timestamp: new Date().toISOString(),
    };
    return HttpResponse.json(responseData);
  }),

  http.get(`${baseUrl}/sales/by_order_type?year=2024`, () => {
    const responseData: Response<OrderSalesRatioType[]> = {
      success: true,
      data: DUMMY_ORDER_TYPES_BY_YEAR_2024,
      timestamp: new Date().toISOString(),
    };
    return HttpResponse.json(responseData);
  }),

  http.get(`${baseUrl}/sales/by_category?year=2024`, () => {
    const responseData: Response<CategorySalesRatioType[]> = {
      success: true,
      data: DUMMY_CATEGORY_SALES_BY_YEAR_2024,
      timestamp: new Date().toISOString(),
    };
    return HttpResponse.json(responseData);
  }),

  http.get(`${baseUrl}/sales/daily`, () => {
    const responseData: Response<DailySalesStatisticsType> = {
      success: true,
      data: DUMMY_DAILY_SALES,
      timestamp: new Date().toISOString(),
    };
    return HttpResponse.json(responseData);
  }),

  http.get(`${baseUrl}/category?pageable:pageable`, () => {
    return HttpResponse.json(CATEGORY_LIST);
  }),

  http.patch(`${baseUrl}/category/:categoryId`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.delete(`${baseUrl}/category/:categoryId`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.post(`${baseUrl}/category`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.get(`${baseUrl}/account?pageable=1`, () => {
    const response: Response<PaginationResponse<AccountType>> = {
      success: true,
      data: {
        content: DUMMY_ACCOUNT_LIST.accounts,
        pageNumber: 1,
        totalPages: 1,
        totalElements: 1,
        pageSize: 1,
        first: true,
        last: true,
      },
      timestamp: new Date().toISOString(),
    };
    return HttpResponse.json(response);
  }),

  http.get(`${baseUrl}/account/detail`, () => {
    const responseData: Response<AccountType> = {
      success: true,
      data: {
        ...DUMMY_MY_INFO,
        accountId: 1,
      },
      timestamp: new Date().toISOString(),
    };
    return HttpResponse.json(responseData);
  }),

  http.patch(`${baseUrl}/account`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.patch(`${baseUrl}/account/change_pw`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.get(`${baseUrl}/kiosk`, () => {
    return HttpResponse.json({
      success: true,
      data: KIOSK_LIST,
      timestamp: new Date().toISOString(),
    });
  }),

  http.post(`${baseUrl}/kiosk`, () => {
    return HttpResponse.json({
      success: true,
      data: {
        kioskId: 1,
        startOrder: 'A',
        name: '키오스크 01',
        isActivate: false,
      },
      timestamp: new Date().toISOString(),
    });
  }),

  http.get(`${baseUrl}/kiosk/:kioskId`, () => {
    return HttpResponse.json({
      success: true,
      data: {
        kioskId: 1,
        startOrder: 'A',
        name: '키오스크 01',
        isActivate: false,
      },
      timestamp: new Date().toISOString(),
    });
  }),

  http.delete(`${baseUrl}/kiosk/:kioskId`, () => {
    return HttpResponse.json({
      success: true,
      data: {},
      timestamp: new Date().toISOString(),
    });
  }),

  http.patch(`${baseUrl}/kiosk/:kioskId`, () => {
    return HttpResponse.json({
      success: true,
      data: {
        kioskId: 1,
        startOrder: 'A',
        name: '키오스크 01',
        isActivate: false,
      },
      timestamp: new Date().toISOString(),
    });
  }),
];
