import { http, HttpResponse } from 'msw';
import { userRole } from './dummies/user';

import { Response } from '@/types/apiResponse';
import {
  CategorySalesRatioType,
  OrderSalesRatioType,
  PaymentSalesRatioType,
} from '@/types/statistics';
import { CATEGORY_LIST } from './dummies/category';
import MENU_LIST from './dummies/menu';
import { OPTION_LIST } from './dummies/option';
import {
  DUMMY_CATEGORY_SALES_BY_YEAR_2024,
  DUMMY_ORDER_TYPES_BY_YEAR_2024,
  DUMMY_PAYMENTS_BY_YEAR_2024,
  DUMMY_SALES_BY_MONTH_2024_05,
  DUMMY_SALES_BY_MONTH_2025_08,
  DUMMY_SALES_BY_YEAR_2024,
  DUMMY_SALES_BY_YEAR_2025,
} from './dummies/statistics';

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

  http.get(`${baseUrl}/option`, () => {
    return HttpResponse.json(OPTION_LIST);
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

  http.get(`${baseUrl}/category?pageable:pageable`, () => {
    return HttpResponse.json(CATEGORY_LIST);
  }),
];
