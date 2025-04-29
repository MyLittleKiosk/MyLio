import type { Meta, StoryObj } from '@storybook/react';
import { BrowserRouter } from 'react-router-dom';
import SideBar from './SideBar';

const meta = {
  title: 'Layout/SideBar',
  component: SideBar,
  parameters: {
    layout: 'fullscreen',
  },
  tags: ['autodocs'],
  argTypes: {
    isSideBarOpen: {
      control: 'boolean',
      defaultValue: true,
    },
  },
  //내부 Link태그 사용을 위한 설정
  decorators: [
    (Story) => (
      <BrowserRouter>
        <Story />
      </BrowserRouter>
    ),
  ],
} satisfies Meta<typeof SideBar>;

export default meta;
type Story = StoryObj<typeof meta>;

//사이드바 오픈 상태
export const Default: Story = {
  args: {
    isSideBarOpen: true,
    setIsSideBarOpen: () => {},
  },
};

//사이드바 닫힌 상태
export const Closed: Story = {
  args: {
    isSideBarOpen: false,
    setIsSideBarOpen: () => {},
  },
};
