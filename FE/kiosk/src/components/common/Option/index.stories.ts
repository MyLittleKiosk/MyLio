import type { Meta, StoryObj } from '@storybook/react';
import Option from './index';

const meta = {
  title: 'Components/Common/Option',
  component: Option,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    optionName: {
      control: 'text',
      description: '옵션 이름',
    },
    price: {
      control: 'number',
      description: '옵션 가격',
    },
  },
} satisfies Meta<typeof Option>;

export default meta;
type Story = StoryObj<typeof meta>;

// 옵션
export const Default: Story = {
  args: {
    optionName: '옵션 이름',
    price: 1000,
  },
};
