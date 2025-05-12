import react from '@vitejs/plugin-react';
// import fs from 'fs';
import { defineConfig } from 'vite';
import tsconfigPaths from 'vite-tsconfig-paths';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  // server: {
  //   https: {
  //     key: fs.readFileSync('./localhost-key.pem'),
  //     cert: fs.readFileSync('./localhost.pem'),
  //   },
  //   port: 3000,
  // },
});
