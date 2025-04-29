import Button from '.';
import type { Meta, StoryObj } from '@storybook/react';

const meta = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof Button>;

export const DefaultButton: Story = {
  args: {
    content: '버튼',
    onClick: () => alert('버튼이 클릭되었습니다.'),
  },
};

export const LongContent: Story = {
  args: {
    content: '긴 텍스트가 있는 버튼',
    onClick: () => alert('버튼이 클릭되었습니다.'),
  },
};
