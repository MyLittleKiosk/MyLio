import axios from 'axios';
const baseUrl = import.meta.env.VITE_PUBLIC_API_URL;

const authClient = axios.create({
  baseURL: baseUrl,
  headers: {
    'Content-Type': 'application/json',
    withCredentials: true,
  },
});

authClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const response = await authClient.post('/auth/refresh');

        if (response.status === 200) {
          return authClient(originalRequest);
        }
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default authClient;
