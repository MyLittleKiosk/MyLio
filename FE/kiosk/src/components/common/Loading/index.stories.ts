import { Meta, StoryObj } from '@storybook/react';
import Loading from './index';

const meta = {
  title: 'Components/common/Loading',
  component: Loading,
  tags: ['autodocs'],
  argTypes: {},
} satisfies Meta<typeof Loading>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};
