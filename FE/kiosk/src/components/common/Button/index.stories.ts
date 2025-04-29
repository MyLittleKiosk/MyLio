import type { Meta, StoryObj } from '@storybook/react';
import Button from './index';

const meta = {
  title: 'Components/Common/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    content: {
      control: 'text',
      description: '버튼에 표시될 텍스트',
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
      description: '버튼의 크기',
    },
    disabled: {
      control: 'boolean',
      description: '버튼 비활성화 여부',
    },
    isLoading: {
      control: 'boolean',
      description: '로딩 상태 여부',
    },
    className: {
      control: 'text',
      description: '추가적인 CSS 클래스',
    },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

// 기본 버튼
export const Default: Story = {
  args: {
    content: '버튼',
    size: 'medium',
  },
};

// 작은 크기 버튼
export const Small: Story = {
  args: {
    content: '작은 버튼',
    size: 'small',
  },
};

// 큰 크기 버튼
export const Large: Story = {
  args: {
    content: '큰 버튼',
    size: 'large',
  },
};

// 비활성화된 버튼
export const Disabled: Story = {
  args: {
    content: '비활성화 버튼',
    disabled: true,
  },
};

// 로딩 상태 버튼
export const Loading: Story = {
  args: {
    content: '로딩 버튼',
    isLoading: true,
  },
};

// 긴 텍스트 버튼
export const LongText: Story = {
  args: {
    content: '이것은 매우 긴 버튼 텍스트입니다',
    size: 'medium',
  },
};
