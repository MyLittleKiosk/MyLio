import { http, HttpResponse } from 'msw';
import MENU_LIST from '@/service/mock/dummies/menu';

const baseUrl = import.meta.env.VITE_PUBLIC_API_URL;

export const handlers = [
  http.get(baseUrl + '/menus', () => {
    return HttpResponse.json(MENU_LIST);
  }),
];
