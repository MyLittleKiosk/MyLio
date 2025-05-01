import { Meta, StoryObj } from '@storybook/react';
import Select from '.';

const meta: Meta<typeof Select> = {
  title: 'Components/Common/Select',
  component: Select,
  tags: ['autodocs'],
  argTypes: {
    options: { control: 'object' },
    label: { control: 'text' },
    selected: { control: 'object' },
    placeholder: { control: 'text' },
    error: { control: 'boolean' },
    disabled: { control: 'boolean' },
    onChange: { action: 'changed', table: { disable: true } },
    className: { control: 'text', table: { disable: true } },
    getOptionLabel: { action: 'changed', table: { disable: true } },
    getOptionValue: { action: 'changed', table: { disable: true } },
  },
} satisfies Meta<typeof Select>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    options: [
      { store_id: 1, store_name: '옵션 1' },
      { store_id: 2, store_name: '옵션 2' },
      { store_id: 3, store_name: '옵션 3' },
    ],
    label: 'Label',
    selected: { store_id: 1, store_name: '옵션 1' },
    placeholder: '옵션을 선택해주세요',
    disabled: false,
  },
};
