import { http, HttpResponse } from 'msw';
import { userRole } from './dummies/user';
const baseUrl = import.meta.env.VITE_PUBLIC_API_URL;
export const handlers = [
  http.get(`${baseUrl}/accounts/role`, () => {
    return HttpResponse.json(userRole);
  }),
];
