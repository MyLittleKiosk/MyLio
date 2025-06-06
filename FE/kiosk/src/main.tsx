import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import { BrowserRouter } from 'react-router-dom';
import './i18n';
const basename = import.meta.env.BASE_URL;
createRoot(document.getElementById('root')!).render(
  // <StrictMode>
  <BrowserRouter basename={basename}>
    <App />
  </BrowserRouter>
  // </StrictMode>
);
