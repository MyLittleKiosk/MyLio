import { Meta, StoryObj } from '@storybook/react';
import Select from '.';

const meta: Meta<typeof Select> = {
  title: 'Components/Common/Select',
  component: Select,
  tags: ['autodocs'],
  argTypes: {
    options: { control: 'object' },
    label: { control: 'text' },
    selected: { control: 'text' },
    placeholder: { control: 'text' },
    error: { control: 'boolean' },
    disabled: { control: 'boolean' },
    onChange: { action: 'changed', table: { disable: true } },
    className: { control: 'text', table: { disable: true } },
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
    disabled: false,
  },
};
