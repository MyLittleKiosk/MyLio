import Table from '.';
import { Meta, StoryObj } from '@storybook/react';
import { MENU_COLUMNS, MENU_LIST } from '@/datas/menuList';

const meta: Meta<typeof Table> = {
  title: 'Components/Common/Table',
  component: Table,
  tags: ['autodocs'],
  argTypes: {
    title: { control: 'text' },
    description: { control: 'text' },
    columns: { control: 'object' },
    data: { control: 'object' },
    className: { control: 'text', table: { disable: true } },
  },
};

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    title: '메뉴 목록',
    description: '총 6개의 메뉴가 있습니다.',
    columns: MENU_COLUMNS,
    data: MENU_LIST.content,
  },
};
