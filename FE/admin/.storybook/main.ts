import type { StorybookConfig } from '@storybook/react-vite';

import { dirname, join } from 'path';
import { mergeConfig } from 'vite';

/**
 * This function is used to resolve the absolute path of a package.
 * It is needed in projects that use Yarn PnP or are set up within a monorepo.
 */
function getAbsolutePath(value: string): string {
  return dirname(require.resolve(join(value, 'package.json')));
}
const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [
    getAbsolutePath('@storybook/addon-essentials'),
    getAbsolutePath('@storybook/addon-onboarding'),
    getAbsolutePath('@chromatic-com/storybook'),
  ],
  framework: {
    name: getAbsolutePath('@storybook/react-vite'),
    options: {},
  },
  viteFinal: async (config) => {
    return mergeConfig(config, {
      define: {
        ...config.define,
        'process.env': {
          ...(config.define?.['process.env'] || {}),
          VITE_IS_STORYBOOK: 'true',
        },
      },
    });
  },
};

export default config;
