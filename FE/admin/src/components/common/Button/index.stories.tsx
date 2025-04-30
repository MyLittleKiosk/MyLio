import Button from '.';
import { Meta, StoryObj } from '@storybook/react';
import IconAccount from '@/assets/icons/IconAccount';

const meta = {
  title: 'Components/Common/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    text: { control: 'text' },
    disabled: { control: 'boolean' },
    error: { control: 'boolean' },
    cancel: { control: 'boolean' },
    icon: { control: 'object', table: { disable: true } },
    onClick: { action: 'clicked', table: { disable: true } },
    className: { control: 'text', table: { disable: true } },
    type: { control: 'select', table: { disable: true } },
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
