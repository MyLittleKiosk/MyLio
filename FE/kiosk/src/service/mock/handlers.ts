import { http, HttpResponse } from 'msw';
import { SEARCH_RESPONSE } from './dummies/Order';
const baseUrl = import.meta.env.VITE_PUBLIC_API_URL;
export const handlers = [
  http.post(`${baseUrl}/order/123`, () => {
    return HttpResponse.json(SEARCH_RESPONSE);
  }),
];
