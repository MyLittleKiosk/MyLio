import Input from './index';
import type { Meta, StoryObj } from '@storybook/react';

const meta: Meta<typeof Input> = {
  title: 'Components/Common/Input',
  component: Input,
  tags: ['autodocs'],
  argTypes: {
    label: { control: 'text' },
    id: { control: 'text', table: { disable: true } },
    placeholder: { control: 'text' },
    type: { control: 'text' },
    value: { control: 'text' },
    error: { control: 'boolean' },
    disabled: { control: 'boolean' },
    onChange: { action: 'changed', table: { disable: true } },
    className: { control: 'text', table: { disable: true } },
  },
} satisfies Meta<typeof Input>;

export default meta;

type Story = StoryObj<typeof Input>;

export const Default: Story = {
  args: {
    label: 'Label',
    id: 'withlabelinput',
    placeholder: 'placeholder',
    type: 'text',
    value: '',
  },
};
