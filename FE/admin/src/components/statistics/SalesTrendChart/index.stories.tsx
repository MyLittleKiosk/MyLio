import { Meta, StoryObj } from '@storybook/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import SalesTrendChart from '.';

const queryClient = new QueryClient();

/**
 * ## 매출 추이 차트
 *
 * 스토리북에서는 **더미 데이터**로 넣어서 테스트합니다. 데이터를 가져오는 시간이 지나면 더미 데이터가 나타납니다.
 *
 * 실제 사용시에는 데이터를 가져오는 것을 권장합니다.
 */
const meta = {
  title: 'Components/Statistics/SalesTrendChart',
  component: SalesTrendChart,
  tags: ['autodocs'],
  parameters: {
    layout: 'fullscreen',
  },
  argTypes: {
    year: {
      control: 'number',
      description: '__필수 입력 옵션__입니다.',
    },
    month: {
      control: 'number',
      description: '0을 입력하면 연도 데이터 그래프를 보여줍니다.',
    },
  },
  decorators: [
    (Story) => (
      <QueryClientProvider client={queryClient}>
        <Story />
      </QueryClientProvider>
    ),
  ],
} satisfies Meta<typeof SalesTrendChart>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    year: 2024,
    month: 1,
  },
  render: (args) => (
    <div className='relative w-full max-h-[300px] min-h-[300px]'>
      <SalesTrendChart {...args} />
    </div>
  ),
};
