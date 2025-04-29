/* eslint-env node */
module.exports = {
  e2e: {
    setupNodeEvents() {
      // implement node event listeners here
    },
    specPattern: '**/*.spec.{js,jsx,ts,tsx}',
    baseUrl: 'http://localhost:5173',
  },

  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite',
    },
    specPattern: '**/*.spec.{js,jsx,ts,tsx}',
  },
};
