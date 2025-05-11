import { Meta, StoryObj } from '@storybook/react';
import PieChart from '.';

const meta = {
  title: 'Components/common/PieChart',
  component: PieChart,
  tags: ['autodocs'],
  argTypes: {
    data: {
      control: 'object',
      description: '차트에 들어갈 데이터 배열',
    },
    labelKey: {
      control: 'text',
      description: '라벨로 사용할 key 이름',
      table: { disable: true },
    },
  },
} satisfies Meta<typeof PieChart>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    data: [
      {
        name: '카드',
        ratio: 0.3,
      },
      {
        name: '현금',
        ratio: 0.5,
      },
      {
        name: '간편 결제',
        ratio: 0.2,
      },
    ],
    labelKey: 'name',
  },
};
