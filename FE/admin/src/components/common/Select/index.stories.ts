import { Meta, StoryObj } from '@storybook/react';
import Select from '.';

const meta = {
  title: 'Components/Common/Select',
  component: Select,
  tags: ['autodocs'],
  argTypes: {
    options: { control: 'object' },
    label: { control: 'text' },
    selected: { control: 'text' },
    placeholder: { control: 'text' },
    className: { control: 'text' },
    error: { control: 'boolean' },
    disabled: { control: 'boolean' },
    onChange: { action: 'changed' },
  },
} satisfies Meta<typeof Select>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    options: [
      { key: '1', value: '옵션 1' },
      { key: '2', value: '옵션 2' },
      { key: '3', value: '옵션 3' },
    ],
    label: 'Label',
    selected: 'option1',
    placeholder: '옵션을 선택해주세요',
    onChange: () => {},
    disabled: false,
  },
};

export const Error: Story = {
  args: {
    ...Default.args,
    error: true,
  },
};

export const Disabled: Story = {
  args: {
    ...Default.args,
    disabled: true,
  },
};
