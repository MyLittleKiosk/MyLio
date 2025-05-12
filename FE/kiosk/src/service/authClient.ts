import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios';

const baseUrl = import.meta.env.VITE_PUBLIC_API_URL;

interface CustomAxiosRequestConfig extends AxiosRequestConfig {
  _retry?: boolean;
}

// 토큰 재발급 진행 여부와 대기 중인 요청들을 저장하는 변수
let isRefreshing = false;
let refreshSubscribers: Array<() => void> = [];

// refresh 완료 후, 대기 중인 모든 요청 재시도
function onRefreshed(): void {
  refreshSubscribers.forEach((cb) => cb());
  refreshSubscribers = [];
}

// refresh token 요청 대기 등록
function subscribeTokenRefresh(cb: () => void): void {
  refreshSubscribers.push(cb);
}

const authClient = axios.create({
  baseURL: baseUrl,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

authClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as CustomAxiosRequestConfig;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // 이미 다른 요청에서 refresh 진행 중이면 대기
      if (isRefreshing) {
        return new Promise((resolve) => {
          subscribeTokenRefresh(() => {
            resolve(authClient(originalRequest));
          });
        });
      }

      isRefreshing = true;
      try {
        const response = await authClient.post('/auth/refresh');

        if (response.status === 200) {
          onRefreshed();
          return authClient(originalRequest);
        }
      } catch (refreshError) {
        // 리프레시 토큰이 만료되었거나 갱신에 실패한 경우
        if ((refreshError as AxiosError).response?.status === 401) {
          // 로그인 페이지로 리다이렉트
          window.location.href = '/login';
        }
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  }
);

export default authClient;
