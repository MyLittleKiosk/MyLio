import axios from 'axios';

const baseUrl = import.meta.env.VITE_PUBLIC_API_URL;

const client = axios.create({
  baseURL: baseUrl,
});

export default client;
