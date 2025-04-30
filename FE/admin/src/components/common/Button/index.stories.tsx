import Button from '.';
import { Meta, StoryObj } from '@storybook/react';
import IconAccount from '@/assets/icons/IconAccount';

const meta = {
  title: 'Components/Common/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    type: { control: 'select' },
    text: { control: 'text' },
    disabled: { control: 'boolean' },
    error: { control: 'boolean' },
    cancel: { control: 'boolean' },
    className: { control: 'text' },
    onClick: { action: 'clicked' },
    icon: { control: 'text' },
  },
} satisfies Meta<typeof Button>;

export default meta;

type Story = StoryObj<typeof meta>;

//텍스트만 있는 버튼
export const Default: Story = {
  args: {
    type: 'button',
    text: 'Button',
  },
};

export const Cancel: Story = {
  args: {
    ...Default.args,
    cancel: true,
  },
};

export const Disabled: Story = {
  args: {
    ...Default.args,
    disabled: true,
  },
};

export const Error: Story = {
  args: {
    ...Default.args,
    error: true,
  },
};
export const OnlyIcon: Story = {
  args: {
    ...Default.args,
    text: '',
    icon: <IconAccount fillColor='white' />,
  },
};

export const IconAndText: Story = {
  args: {
    ...Default.args,
    text: 'Button',
    icon: <IconAccount fillColor='white' />,
  },
};
