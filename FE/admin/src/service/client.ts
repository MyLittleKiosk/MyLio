import axios from 'axios';

const baseUrl = import.meta.env.VITE_PUBLIC_API_URL;

const client = axios.create({
  baseURL: baseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

export default client;
