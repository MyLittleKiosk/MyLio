import { http, HttpResponse } from 'msw';
import { userRole } from './dummies/user';

import {
  DUMMY_SALES_BY_MONTH_2024_05,
  DUMMY_SALES_BY_MONTH_2025_08,
  DUMMY_SALES_BY_YEAR_2024,
  DUMMY_SALES_BY_YEAR_2025,
} from './dummies/statistics';
import MENU_LIST from './dummies/menu';
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

  http.get(baseUrl + '/menus', () => {
    return HttpResponse.json(MENU_LIST);
  }),
  http.get(`${baseUrl}/accounts/role`, () => {
    return HttpResponse.json(userRole);
  }),
];
